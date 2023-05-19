# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0
from __future__ import annotations

import typing as t
from datetime import datetime, timezone

from cacheyou.cache import BaseCache

if t.TYPE_CHECKING:

    class RedisConn(t.Protocol):
        def get(self, key: str) -> bytes | None:
            ...

        def set(self, key: str, value: bytes) -> None:
            ...

        def setex(self, key: str, expires: int, value: bytes) -> None:
            ...

        def delete(self, key: str) -> None:
            ...

        def keys(self) -> t.Iterable[str]:
            ...


class RedisCache(BaseCache):
    def __init__(self, conn: RedisConn) -> None:
        self.conn = conn

    def get(self, key: str) -> bytes | None:
        return self.conn.get(key)

    def set(self, key: str, value: bytes, expires: int | datetime | None = None) -> None:
        if not expires:
            self.conn.set(key, value)
        elif isinstance(expires, datetime):
            now_utc = datetime.now(timezone.utc)
            if expires.tzinfo is None:
                now_utc = now_utc.replace(tzinfo=None)
            delta = expires - now_utc
            self.conn.setex(key, int(delta.total_seconds()), value)
        else:
            self.conn.setex(key, expires, value)

    def delete(self, key: str) -> None:
        self.conn.delete(key)

    def clear(self) -> None:
        """Helper for clearing all the keys in a database. Use with
        caution!"""
        for key in self.conn.keys():
            self.conn.delete(key)

    def close(self) -> None:
        """Redis uses connection pooling, no need to close the connection."""
        pass
