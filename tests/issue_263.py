#!/usr/bin/env python3
import logging
import sys

import requests

import cacheyou
from cacheyou.cache import DictCache
from cacheyou.heuristics import BaseHeuristic

clogger = logging.getLogger("cachecontrol")
clogger.addHandler(logging.StreamHandler())
clogger.setLevel(logging.DEBUG)


class NoAgeHeuristic(BaseHeuristic):
    def update_headers(self, response):
        if "cache-control" in response.headers:
            del response.headers["cache-control"]


cache_adapter = cacheyou.CacheControlAdapter(
    DictCache(), cache_etags=True, heuristic=NoAgeHeuristic()
)


session = requests.Session()
session.mount("https://", cache_adapter)


def log_resp(resp):
    return

    print(f"{resp.status_code} {resp.request.method}")
    for k, v in response.headers.items():
        print(f"{k}: {v}")


for _ in range(2):
    response = session.get("https://api.github.com/repos/sigmavirus24/github3.py/pulls/1033")
    log_resp(response)
    print(f"Content length: {len(response.content)}")
    print(response.from_cache)  # type: ignore[attr-defined]
    if len(response.content) == 0:
        sys.exit(1)
