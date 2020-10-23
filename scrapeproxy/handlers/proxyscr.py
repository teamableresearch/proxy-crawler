import requests
from bs4 import BeautifulSoup
import re
import traceback


class Proxy_list_proxyscrp:
    """
    proxy list from https://www.proxyscrape.com/free-proxy-list
    """
    def get_proxy_list(self, limit=-1, anonymous=True, https=True, google=False, country=None):
        """
        get proxy list from https://www.proxyscrape.com/free-proxy-list

        [params]:

        :limit: Count of proxies to return, default is -1
        :anonymous: Boolean value to filter only anonimising proxies, default is True
        :https: Boolean value to filter proxies with https, default is True
        :google: Boolean value to filter proxies with google access, default is False
        :country: country code, supported only US and UK , default is US
        """
        url = "https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000"
        try:
            # if country == "US":
            #     url += "&country=US"
            # if country == "UK":
            #     url += "&country=UK"
            # else:
            #     url += "&country=all"
            # if https:
            #     url += "&ssl=yes"
            # else:
            #     url += "&ssl=all"
            # # filters
            # urls = []
            # if anonymous:
            #     urls.append(url+"&anonymity=elite")
            #     urls.append(url+"&anonymity=anonymous")
            # else:
            #     urls = [url+"&anonymity=all"]
            
            # IMPORTANT seems all are https and anonymous
            urls = ["https://api.proxyscrape.com/?request=getproxies&proxytype=http&timeout=10000&country=all&ssl=all&anonymity=all"]
            for i in urls:
                proxy_dicts = self.scrape_proxies(i)
            proxy_dicts = proxy_dicts[:limit]
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []

    def scrape_proxies(self, url):
        try:
            result = requests.get(url)
            if result.status_code != 200:
                print("Seems proxyscrape service is down! \n" + result.reason)
                return []
            res_list = result.content.split()
            proxy_list = []
            for line in res_list:
                proxy_string = line
                proxy = []
                proxy.append({
                    "http": proxy_string,
                    "https": proxy_string
                })
                proxy.append(proxy_string)
                proxy.append("https://www.proxyscrape.com/free-proxy-list")
                proxy_list.append(proxy)
            header = ["proxy", "proxy_string", "source"]
            proxy_dicts = [dict(zip(header, proxy)) for proxy in proxy_list]
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []
