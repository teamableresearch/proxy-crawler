from .proxy_sources import proxy_sources
from tqdm import tqdm

USED_PROXIES = []
CACHED_PROXIES = []


def get_proxies(limit=None, filter_sources=[], anonymous=True, https=True, google=False, clear_used_proxies=False,
                country=None):
    """
    Get new fresh proxy from public sources
    [params]:

    :filter_sources: list of source names to use the proxies from
                    "best" --> https://www.us-proxy.org/
                    "pub"  --> http://pubproxy.com
                    "hmn"  --> https://hidemyna.me/en
    :limit: Count of proxies to return, default is -1
    :anonymous: Boolean value to filter only anonimising proxies, default is True
    :https: Boolean value to filter proxies with https, default is True
    :google: Boolean value to filter proxies with google access, default is False
    :clear_used_proxies: Boolean value to clear used list of proxies, default is False
    :country: country code, supported only US , default is None

    [WARNING] not all params are supported for every source

    [return]:
    dict object with keys
        - info : all info about proxy
        - proxy : dict object to use for requests
        - proxy_string : "host:port" formatted string
        - source : source of proxy
    """
    global USED_PROXIES
    global CACHED_PROXIES

    # make the function more robust
    if limit and limit < 0:
        limit = None

    # Clear the memory of used proxies (USED_PROXIES)
    if clear_used_proxies:
        USED_PROXIES = []

    # initialize the list variable which we will (accumulate and return) the CACHED_PROXIES(unused proxies).
    proxy_list = []

    # Extend(add) the unused accumulated proxies from CACHED_PROXIES, and set the CACHED_PROXIES to empty.
    proxy_list.extend(CACHED_PROXIES)
    CACHED_PROXIES = []

    # If the proxies we have are enough (which were loaded from CACHED_PROXIES) then update the CACHED_PROXIES and
    # return the needed amount of proxies
    if len(proxy_list) != 0 and limit and limit <= len(proxy_list):
        CACHED_PROXIES = proxy_list[limit:]
        return proxy_list[:limit]

    eligible_sources = list(proxy_sources)

    if filter_sources:
        eligible_sources = [source for source in proxy_sources if source["id"] in filter_sources]

    for source in tqdm(eligible_sources):
        proxies = source["handler"]().get_proxy_list(limit=-1, anonymous=anonymous,
                                                     https=https, google=google, country=country)

        # Check if the proxies are not already USED, when scraping the same source.
        proxies = [proxy for proxy in proxies if proxy["proxy_string"] not in USED_PROXIES]

        proxy_list.extend(proxies)

        # make all proxies unique (as different sources can have the same proxy)
        proxy_list = list({proxy['proxy_string']: proxy for proxy in proxy_list}.values())

        # if limit and limit-len(proxy_list) <= 0:
        #     break
        print("[INFO] processed source : " + source["source"] + ", found proxies : " + str(len(proxies)))

    # Add proxies that will be returned as USED proxies.
    USED_PROXIES.extend([proxy["proxy_string"] for proxy in proxy_list[:limit]])

    # Set the rest of proxies(which will not be return) as CACHED_PROXIES for next call.
    # If limit is None, then set CACHED_PROXIES to empty, as all proxies will be returned.
    if limit:
        CACHED_PROXIES = proxy_list[limit:]
    else:
        CACHED_PROXIES = []

    return proxy_list[:limit]
