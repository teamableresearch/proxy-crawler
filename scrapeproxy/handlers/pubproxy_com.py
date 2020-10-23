import requests
import traceback


class Proxy_list_pubproxy:
    """
    proxy list from http://pubproxy.com API
    """

    def get_proxy_list(self, limit=-1, anonymous=True, https=True, google=False, country=None):
        """
        get proxy list from "http://pubproxy.com"

        [params]:

        :limit: Count of proxies to return, default is -1
        :anonymous: Boolean value to filter only anonimising proxies, default is True
        :https: Boolean value to filter proxies with https, default is True
        :google: Boolean value to filter proxies with google access, default is False
        :country: country code, supported only US , default is US
        """
        try:
            url = "http://pubproxy.com/api/proxy?format=json&type=http"
            if not limit or limit < 0:
                # max limit for free users is 5
                limit = 5
            url += "&limit="+str(limit)
            if country:
                url += "&country="+country
            if https:
                url += "&https=true"
            if google:
                url += "&google=true"
            if anonymous:
                url += "&level=anonymous,elite"

            proxy_dicts = self.scrape_proxies(url)
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []

    def get_proxy_dict(self, proxy_string):
        return {
            "http": proxy_string,
            "https": proxy_string
        }

    def scrape_proxies(self, url):
        try:
            result = requests.get(url)
            if result.status_code != 200:
                print("Seems pub-proxy service is down! \n" + result.reason)
                return []
            result_json = result.json().get("data", [])
            proxy_list = [[proxy, self.get_proxy_dict(proxy["ipPort"]), proxy["ipPort"], "http://pubproxy.com"]
                          for proxy in result_json]
            header = ["info", "proxy", "proxy_string", "source"]
            proxy_dicts = [dict(zip(header, proxy)) for proxy in proxy_list]
            return proxy_dicts
        except Exception:
            print("Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []
