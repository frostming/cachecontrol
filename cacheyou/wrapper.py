# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import typing as t

from cacheyou.adapter import CacheControlAdapter
from cacheyou.cache import DictCache

if t.TYPE_CHECKING:
    from requests import Session

    from cacheyou.cache import BaseCache
    from cacheyou.controller import CacheController
    from cacheyou.heuristics import BaseHeuristic
    from cacheyou.serialize import Serializer


def CacheControl(
    sess: Session,
    cache: BaseCache | None = None,
    cache_etags: bool = True,
    serializer: Serializer | None = None,
    heuristic: BaseHeuristic | None = None,
    controller_class: type[CacheController] | None = None,
    adapter_class: type[CacheControlAdapter] | None = None,
    cacheable_methods: t.Collection[str] | None = None,
):
    cache = DictCache() if cache is None else cache
    adapter_class = adapter_class or CacheControlAdapter
    adapter = adapter_class(
        cache,
        cache_etags=cache_etags,
        serializer=serializer,
        heuristic=heuristic,
        controller_class=controller_class,
        cacheable_methods=cacheable_methods,
    )
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    return sess
