# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

from unittest.mock import Mock

import pytest
from requests import Session

from cacheyou.adapter import CacheControlAdapter
from cacheyou.cache import DictCache
from cacheyou.wrapper import CacheControl


def use_wrapper():
    print("Using helper")
    sess = CacheControl(Session())
    return sess


def use_adapter():
    print("Using adapter")
    sess = Session()
    sess.mount("http://", CacheControlAdapter())
    return sess


@pytest.fixture(params=[use_adapter, use_wrapper])
def sess(url, request):
    sess = request.param()
    sess.get(url)
    yield sess

    # closing session object
    sess.close()


class TestSessionActions:
    def test_get_caches(self, url, sess):
        r2 = sess.get(url)
        assert r2.from_cache is True

    def test_get_with_no_cache_does_not_cache(self, url, sess):
        r2 = sess.get(url, headers={"Cache-Control": "no-cache"})
        assert not r2.from_cache

    def test_put_invalidates_cache(self, url, sess):
        r2 = sess.put(url, data={"foo": "bar"})
        sess.get(url)
        assert not r2.from_cache

    def test_patch_invalidates_cache(self, url, sess):
        r2 = sess.patch(url, data={"foo": "bar"})
        sess.get(url)
        assert not r2.from_cache

    def test_delete_invalidates_cache(self, url, sess):
        r2 = sess.delete(url)
        sess.get(url)
        assert not r2.from_cache

    def test_close(self):
        cache = Mock(spec=DictCache)
        sess = Session()
        sess.mount("http://", CacheControlAdapter(cache))

        sess.close()
        assert cache.close.called
