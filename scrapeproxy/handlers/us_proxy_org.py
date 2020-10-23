import requests
from bs4 import BeautifulSoup
import re
import traceback


class Proxy_list_proxyorg:
    """
    proxy list from https://www.us-proxy.org/
    """
    def get_proxy_list(self, limit=-1, anonymous=True, https=True, google=False, country=None):
        """
        get proxy list from "https://www.us-proxy.org/"

        [params]:

        :limit: Count of proxies to return, default is -1
        :anonymous: Boolean value to filter only anonimising proxies, default is True
        :https: Boolean value to filter proxies with https, default is True
        :google: Boolean value to filter proxies with google access, default is False
        :country: country code, supported only US , default is US
        """
        try:
            if country == "US":
                url = "https://www.us-proxy.org/"
            if country == "UK":
                url = "https://free-proxy-list.net/uk-proxy.html"
            else:
                url = "https://free-proxy-list.net/"
            proxy_dicts = self.scrape_proxies(url)
            # filters
            if anonymous:
                proxy_dicts = [proxy for proxy in proxy_dicts
                               if proxy["info"]["Anonymity"] in ["anonymous", "elite proxy"]]
            if https:
                proxy_dicts = [proxy for proxy in proxy_dicts
                               if proxy["info"]["Https"] == "yes"]
            if google:
                proxy_dicts = [proxy for proxy in proxy_dicts
                               if proxy["info"]["Google"] == "yes"]
            proxy_dicts = proxy_dicts[:limit]
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []

    def scrape_proxies(self, url):
        try:
            result = requests.get(url)
            if result.status_code != 200:
                print("Seems us-proxy service is down! \n" + result.reason)
                return []
            content = BeautifulSoup(result.content, features="html.parser")
            table = content.find("table")
            header_line = list(table.children)[0]
            header = re.findall(r"<th[^\>]*>([^\<\>]*)</th>", str(header_line))
            header.append("proxy")
            proxy_table = list(table.children)[1]
            proxy_list = []
            for line in proxy_table.children:
                parsed_proxy = re.findall(r"<td[^\>]*>([^\<\>]*)</td>", str(line))
                proxy_info = dict(zip(header, parsed_proxy))
                proxy = [proxy_info]
                proxy_string = proxy_info["IP Address"] + ":" + proxy_info["Port"]
                proxy.append({
                    "http": proxy_string,
                    "https": proxy_string
                })
                proxy.append(proxy_string)
                proxy.append("https://www.us-proxy.org/")
                proxy_list.append(proxy)
            header = ["info", "proxy", "proxy_string", "source"]
            proxy_dicts = [dict(zip(header, proxy)) for proxy in proxy_list]
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []
