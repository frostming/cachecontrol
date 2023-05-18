# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

import sys

import pytest
from requests import Session

from cacheyou import CacheControl
from cacheyou.caches import FileCache
from cacheyou.filewrapper import CallbackFileWrapper


class Test39:
    @pytest.mark.skipif(
        sys.version.startswith("2"), reason="Only run this for python 3.x"
    )
    def test_file_cache_recognizes_consumed_file_handle(self, url):
        s = CacheControl(Session(), FileCache("web_cache"))
        the_url = url + "cache_60"
        s.get(the_url)
        r = s.get(the_url)
        assert r.from_cache
        s.close()


def test_getattr_during_gc():
    s = CallbackFileWrapper(None, None)
    # normal behavior:
    with pytest.raises(AttributeError):
        s.x

    # this previously had caused an infinite recursion
    vars(s).clear()  # gc does this.
    with pytest.raises(AttributeError):
        s.x
