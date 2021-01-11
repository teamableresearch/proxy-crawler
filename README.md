# Getting proxies from public sources

### How to install
`pip install proxy-crawler/`

### How to use

Usage
```
import requests
from scrapeproxy import proxies
# example of filters
# proxy = proxies.get_proxies(limit=1, filter_sources=["best", "hmn", "pub"])
proxy = proxies.get_proxies()
requests.get(url, proxies=proxy[0]["proxy"])
...
```
proxy output example (info fields are custom for each source)
```
[{'info': {'IP Address': '35.221.107.127',
   'Port': '3128',
   'Code': 'US',
   'Country': 'United States',
   'Anonymity': 'anonymous',
   'Google': 'no',
   'Https': 'yes',
   'Last Checked': '1 minute ago'},
  'proxy': {'http': '35.221.107.127:3128', 'https': '35.221.107.127:3128'},
  'proxy_string': '35.221.107.127:3128',
  'source': 'https://www.us-proxy.org/'}]
```
NOTE : by default it holds cache(session-wide, so new import new cache) and does not return the same proxy multiple times,
but you can clear cache with `empty_cache` param, for more details type`proxies.get_proxies?`

NOTE : we are trying to crawl large number of proxies so the quality may be not the best, we suggest to set short timeouts (ex. 3 seconds) and use that to ignore the proxies which are too slow or unresponsive.

## Supported sources

Check [this file](./scrapeproxy/proxy_sources.py)

## How to contribute

Add more sources for proxies.

1. Add file for your source in handlers folder.
2. Write class with method `get_proxy_list`, with params
`(limit=-1, anonymous=True, https=True, google=False)`
which returns list of dicts with format.
```
{
  "info" : dict with info about proxy,
  "proxy" : dict with http and https keys
  "proxy_string" : string with format host:port
  "source" : source of proxy
}
```
3. Go to `proxy_sources.py` and add your source with same format in `proxy_sources` list.
[NOTE] order is very important and denotes importance and qualiry of source.
4. Nothing else, thanks ;).
5. One more step, please write docstrings and comment your code.



## TODO
1. We have decided to try having proxy pool instead of module (to easier overcome the limits)
2. add more sources and maybe verify them
3. test and compare proxy-pool vs proxy-module approaches
