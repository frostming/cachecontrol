
# CacheYou

[![Latest Version](https://img.shields.io/pypi/v/cacheyou.svg)](https://pypi.python.org/pypi/cacheyou)
[![CI](https://github.com/frostming/cacheyou/actions/workflows/tests.yml/badge.svg)](https://github.com/frostming/cacheyou/actions/workflows/tests.yml)

CacheYou is a fork of [CacheControl] which is a port of the caching algorithms in httplib2 for use with
requests session object.

[CacheControl]: https://github.com/ionrock/cachecontrol

## Quickstart

```python
import requests
from cacheyou import CacheControl

sess = requests.session()
cached_sess = CacheControl(sess)

response = cached_sess.get('http://google.com')
```

If the URL contains any caching based headers, it will cache the
result in a simple dictionary.

For more info, check out the [docs]

[docs]: http://cacheyou.readthedocs.org/en/latest/
