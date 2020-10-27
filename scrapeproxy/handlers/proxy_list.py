import requests
import traceback


class Proxy_list_proxylist:
    """
    proxy list from https://www.proxy-list.download/api/v1/get API
    """

    def get_proxy_list(self, limit=None, anonymous=True, https=True, google=False, country=None):
        """
        get proxy list from "https://www.proxy-list.download/api/v1/get"

        [params]:
        :anonymous: Boolean value to filter only anonimising proxies, default is True
        :https: Boolean value to filter proxies with https, default is True
        :country: country code, supported only US , default is None
        """
        try:
            proxy_dicts = []
            url = "https://www.proxy-list.download/api/v1/get"
            # url_elite = "https://www.proxy-list.download/api/v1/get?type=http&anon=elite"
            # url_anonymous = "https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous"
            if https:
                url += "?type=https"
            else:
                url += "?type=http"

            if country:
                url += "&country="+country

            if anonymous:
                url_elite = url+"&anon=elite"
                proxy_dicts += self.scrape_proxies(url_elite, anonymity='elite')

                url_anonymous = url+"&anon=anonymous"
                proxy_dicts += self.scrape_proxies(url_anonymous, anonymity='anonymous')
            else:
                proxy_dicts += self.scrape_proxies(url, anonymity='xary')

            proxy_dicts = list({p['proxy_string']: p for p in proxy_dicts}.values())
            return proxy_dicts
        except Exception:
            print("[ERROR] Unexpected error : TRACEBACK \n", traceback.format_exc())
            return []

    def scrape_proxies(self, url, anonymity):
        try:
            result = requests.get(url)
            if result.status_code != 200:
                print("[ERROR] Seems pub-proxy service is down! \n" + result.reason)
                return []
            proxies = result.text.split()
            proxies = [{
                'proxy': {"https": proxy, "http": proxy},
                'source': 'proxy-list.download',
                'proxy_string': proxy,
                'info': {'Anonymity': anonymity}} for proxy in proxies if proxy]

            return proxies
        except:
            print("[ERROR] https://www.proxy-list.download IS NOT WORKING PROPERLY")
            return []
