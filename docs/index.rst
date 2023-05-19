..
  SPDX-FileCopyrightText: SPDX-FileCopyrightText: 2015 Eric Larson

  SPDX-License-Identifier: Apache-2.0

.. CacheYou documentation master file, created by
   sphinx-quickstart on Mon Nov  4 15:01:23 2013.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to CacheYou's documentation!
========================================

CacheYou is a maintained fork of CacheControl, which is a port of httplib2's caching algorithms.
You can read the original documentation `here <https://cachecontrol.readthedocs.io/en/latest/>`_.

It was written because httplib2's better support for caching is often
mitigated by its lack of thread-safety. The same is true of requests in
terms of caching.


Install
=======

CacheYou is available from PyPI_. You can install it with pip_ ::

  $ pip install CacheYou

Some of the included cache storage classes have external
requirements. See :doc:`storage` for more info.



Quick Start
===========

For the impatient, here is how to get started using CacheYou:

.. code-block:: python

  import requests

  from cacheyou import CacheControl


  sess = requests.session()
  cached_sess = CacheControl(sess)

  response = cached_sess.get('http://google.com')


This uses a thread-safe in-memory dictionary for storage.


Tests
=====

The tests are all in ``cacheyou/tests`` and are runnable by ``pytest``.


Disclaimers
===========

CacheYou is relatively new and might have bugs. I have made an
effort to faithfully port the tests from httplib2 to CacheYou, but
there is a decent chance that I've missed something. Please file bugs
if you find any issues!

With that in mind, CacheYou has been used sucessfully in
production environments, replacing httplib2's usage.

If you give it a try, please let me know of any issues.


.. _httplib2: https://github.com/httplib2/httplib2
.. _requests: http://docs.python-requests.org/
.. _Editing the Web: http://www.w3.org/1999/04/Editing/
.. _PyPI: https://pypi.python.org/pypi/CacheYou/
.. _pip: http://www.pip-installer.org/


Contents:

.. toctree::
   :maxdepth: 2

   usage
   storage
   etags
   custom_heuristics
   tips
   release_notes



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
