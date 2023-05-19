# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import base64
import io
import json
import pickle
import typing as t
import zlib

import msgpack
from requests.structures import CaseInsensitiveDict
from urllib3 import HTTPResponse

if t.TYPE_CHECKING:
    from requests import PreparedRequest


def _b64_decode_bytes(b: str) -> bytes:
    return base64.b64decode(b.encode("ascii"))


def _b64_decode_str(s: str) -> str:
    return _b64_decode_bytes(s).decode("utf8")


_default_body_read = object()


class Serializer:
    def dumps(
        self, request: PreparedRequest, response: HTTPResponse, body: bytes | None = None
    ) -> bytes:
        response_headers = CaseInsensitiveDict(response.headers)

        if body is None:
            # When a body isn't passed in, we'll read the response. We
            # also update the response with a new file handler to be
            # sure it acts as though it was never read.
            body = response.read(decode_content=False)
            response._fp = io.BytesIO(body)  # type: ignore[attr-defined]
            response.length_remaining = len(body)

        data = {
            "response": {
                "body": body,  # Empty bytestring if body is stored separately
                "headers": {str(k): str(v) for k, v in response.headers.items()},
                "status": response.status,
                "version": response.version,
                "reason": str(response.reason),
                "decode_content": response.decode_content,
            }
        }

        # Construct our vary headers
        data["vary"] = {}
        if "vary" in response_headers:
            varied_headers = response_headers["vary"].split(",")
            for header in varied_headers:
                header = str(header).strip()
                header_value = request.headers.get(header, None)
                if header_value is not None:
                    header_value = str(header_value)
                data["vary"][header] = header_value

        return b",".join([b"cc=4", msgpack.dumps(data, use_bin_type=True)])

    def loads(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        # Short circuit if we've been given an empty set of data
        if not data:
            return None

        # Determine what version of the serializer the data was serialized
        # with
        try:
            ver, data = data.split(b",", 1)
        except ValueError:
            ver = b"cc=0"

        # Make sure that our "ver" is actually a version and isn't a false
        # positive from a , being in the data stream.
        if ver[:3] != b"cc=":
            data = ver + data
            ver = b"cc=0"

        # Get the version number out of the cc=N
        ver_str = ver.split(b"=", 1)[-1].decode("ascii")

        # Dispatch to the actual load method for the given version
        try:
            return getattr(self, f"_loads_v{ver_str}")(request, data, body_file)

        except AttributeError:
            # This is a version we don't have a loads function for, so we'll
            # just treat it as a miss and return None
            return None

    def prepare_response(
        self, request: PreparedRequest, cached: dict, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        """Verify our vary headers match and construct a real urllib3
        HTTPResponse object.
        """
        # Special case the '*' Vary value as it means we cannot actually
        # determine if the cached response is suitable for this request.
        # This case is also handled in the controller code when creating
        # a cache entry, but is left here for backwards compatibility.
        if "*" in cached.get("vary", {}):
            return None

        # Ensure that the Vary headers for the cached response match our
        # request
        for header, value in cached.get("vary", {}).items():
            if request.headers.get(header, None) != value:
                return None

        body_raw = cached["response"].pop("body")

        headers: t.MutableMapping[str, str] = CaseInsensitiveDict(
            data=cached["response"]["headers"]
        )
        if headers.get("transfer-encoding", "") == "chunked":
            headers.pop("transfer-encoding")

        cached["response"]["headers"] = headers

        try:
            if body_file is None:
                body_file = io.BytesIO(body_raw)
        except TypeError:
            # This can happen if cachecontrol serialized to v1 format (pickle)
            # using Python 2. A Python 2 str(byte string) will be unpickled as
            # a Python 3 str (unicode string), which will cause the above to
            # fail with:
            #
            #     TypeError: 'str' does not support the buffer interface
            body_file = io.BytesIO(body_raw.encode("utf8"))

        return HTTPResponse(body=body_file, preload_content=False, **cached["response"])

    def _loads_v0(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        # The original legacy cache data. This doesn't contain enough
        # information to construct everything we need, so we'll treat this as
        # a miss.
        return None

    def _loads_v1(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        try:
            cached = pickle.loads(data)
        except ValueError:
            return None

        return self.prepare_response(request, cached, body_file)

    def _loads_v2(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        assert body_file is None
        try:
            cached = json.loads(zlib.decompress(data).decode("utf8"))
        except (ValueError, zlib.error):
            return None

        # We need to decode the items that we've base64 encoded
        cached["response"]["body"] = _b64_decode_bytes(cached["response"]["body"])
        cached["response"]["headers"] = {
            _b64_decode_str(k): _b64_decode_str(v) for k, v in cached["response"]["headers"].items()
        }
        cached["response"]["reason"] = _b64_decode_str(cached["response"]["reason"])
        cached["vary"] = {
            _b64_decode_str(k): _b64_decode_str(v) if v is not None else v
            for k, v in cached["vary"].items()
        }

        return self.prepare_response(request, cached, body_file)

    def _loads_v3(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        # Due to Python 2 encoding issues, it's impossible to know for sure
        # exactly how to load v3 entries, thus we'll treat these as a miss so
        # that they get rewritten out as v4 entries.
        return None

    def _loads_v4(
        self, request: PreparedRequest, data: bytes, body_file: t.IO[bytes] | None = None
    ) -> HTTPResponse | None:
        try:
            cached = msgpack.loads(data, raw=False)
        except ValueError:
            return None

        return self.prepare_response(request, cached, body_file)
