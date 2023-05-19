# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

import logging
from argparse import ArgumentParser, Namespace

import requests

from cacheyou.adapter import CacheControlAdapter
from cacheyou.cache import DictCache
from cacheyou.controller import logger


def setup_logging() -> None:
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    logger.addHandler(handler)


def get_session() -> requests.Session:
    adapter = CacheControlAdapter(DictCache(), cache_etags=True, serializer=None, heuristic=None)
    sess = requests.Session()
    sess.mount("http://", adapter)
    sess.mount("https://", adapter)

    sess.cache_controller = adapter.controller  # type:ignore[attr-defined]
    return sess


def get_args() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument("url", help="The URL to try and cache")
    return parser.parse_args()


def main() -> None:
    args = get_args()
    sess = get_session()

    # Make a request to get a response
    resp = sess.get(args.url)

    # Turn on logging
    setup_logging()

    # try setting the cache
    sess.cache_controller.cache_response(resp.request, resp.raw)  # type: ignore[attr-defined]

    # Now try to get it
    if sess.cache_controller.cached_request(resp.request):  # type: ignore[attr-defined]
        print("Cached!")
    else:
        print("Not cached :(")


if __name__ == "__main__":
    main()
