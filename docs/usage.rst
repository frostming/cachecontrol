..
  SPDX-FileCopyrightText: SPDX-FileCopyrightText: 2015 Eric Larson

  SPDX-License-Identifier: Apache-2.0

===============
 Using CacheYou
===============

CacheYou assumes you are using a `requests.Session` for your
requests. If you are making ad-hoc requests using `requests.get` then
you probably are not terribly concerned about caching.

There are two way to use CacheYou, via the wrapper and the
adapter.


Wrapper
=======

The easiest way to use CacheYou is to utilize the basic
wrapper. Here is an example: ::

  import requests
  import cacheyou

  sess = cacheyou.CacheControl(requests.Session())
  resp = sess.get('http://google.com')

This uses the default cache store, a thread safe in-memory dictionary.


Adapter
=======

The other way to use CacheYou is via a requests `Transport
Adapter`_.

Here is how the adapter works: ::

  import requests
  import cacheyou

  sess = requests.Session()
  sess.mount('http://', cacheyou.CacheControlAdapter())

  resp = sess.get('http://google.com')


Under the hood, the wrapper method of using CacheControl mentioned
above is the same as this example.


Use a Different Cache Store
===========================

Both the wrapper and adapter classes allow providing a custom cache
store object for storing your cached data. Here is an example using
the provided `FileCache` from CacheYou: ::

  import requests

  from cacheyou import CacheControl

  # NOTE: This requires filelock be installed
  from cacheyou.caches import FileCache

  sess = CacheControl(requests.Session(),
                      cache=FileCache('.webcache'))


The `FileCache` will create a directory called `.webcache` and store a
file for each cached request.



.. _Transport Adapter: http://docs.python-requests.org/en/latest/user/advanced/#transport-adapters
