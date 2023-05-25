# SPDX-FileCopyrightText: 2015 Eric Larson, 2023 Frost Ming
#
# SPDX-License-Identifier: Apache-2.0

"""CacheControl import Interface.

Make it easy to import from cachecontrol without long namespaces.
"""
import logging

from cacheyou.adapter import CacheControlAdapter
from cacheyou.controller import CacheController
from cacheyou.wrapper import CacheControl

__version__ = "23.3"

logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = ("CacheControl", "CacheControlAdapter", "CacheController")
