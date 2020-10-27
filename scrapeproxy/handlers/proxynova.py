import requests
import pandas as pd
import re
import traceback
from tqdm import tqdm

countries = ['country-af', 'country-ax', 'country-al', 'country-dz', 'country-as', 'country-ad', 'country-zw'
             'country-ao', 'country-ai', 'country-ag', 'country-ar', 'country-am', 'country-aw', 'country-au',
             'country-at', 'country-az', 'country-bh', 'country-bd', 'country-bb', 'country-by', 'country-be',
             'country-bz', 'country-bj', 'country-bm', 'country-bt', 'country-bo', 'country-ba', 'country-bw',
             'country-br', 'country-io', 'country-vg', 'country-bn', 'country-bg', 'country-bf', 'country-bi',
             'country-kh', 'country-cm', 'country-ca', 'country-cv', 'country-ky', 'country-cf', 'country-td',
             'country-cl', 'country-cn', 'country-co', 'country-ck', 'country-cr', 'country-ci', 'country-hr',
             'country-cu', 'country-cy', 'country-cz', 'country-cd', 'country-dk', 'country-dj', 'country-dm',
             'country-do', 'country-ec', 'country-eg', 'country-sv', 'country-gq', 'country-er', 'country-ee',
             'country-et', 'country-fo', 'country-fm', 'country-fj', 'country-fi', 'country-fr', 'country-gf',
             'country-pf', 'country-ga', 'country-ge', 'country-de', 'country-gh', 'country-gi', 'country-gr',
             'country-gl', 'country-gd', 'country-gp', 'country-gu', 'country-gt', 'country-gg', 'country-gn',
             'country-gw', 'country-gy', 'country-ht', 'country-hn', 'country-hk', 'country-hu', 'country-is',
             'country-in', 'country-id', 'country-ir', 'country-iq', 'country-ie', 'country-im', 'country-il',
             'country-it', 'country-jm', 'country-jp', 'country-je', 'country-jo', 'country-kz', 'country-ke',
             'country-ki', 'country-kw', 'country-kg', 'country-la', 'country-lv', 'country-lb', 'country-ls',
             'country-lr', 'country-ly', 'country-li', 'country-lt', 'country-lu', 'country-mo', 'country-mk',
             'country-mg', 'country-mw', 'country-my', 'country-mv', 'country-ml', 'country-mt', 'country-mh',
             'country-mr', 'country-mu', 'country-mx', 'country-md', 'country-mc', 'country-mn', 'country-me',
             'country-ms', 'country-ma', 'country-mz', 'country-mm', 'country-na', 'country-nr', 'country-np',
             'country-nl', 'country-an', 'country-nc', 'country-nz', 'country-ni', 'country-ne', 'country-ng',
             'country-nu', 'country-nf', 'country-mp', 'country-kp', 'country-no', 'country-om', 'country-pk',
             'country-pw', 'country-ps', 'country-pa', 'country-pg', 'country-py', 'country-pe', 'country-ph',
             'country-pl', 'country-pt', 'country-pr', 'country-qa', 'country-cg', 'country-re', 'country-ro',
             'country-ru', 'country-rw', 'country-kn', 'country-lc', 'country-mf', 'country-pm', 'country-vc',
             'country-ws', 'country-sm', 'country-sa', 'country-sn', 'country-rs', 'country-sc', 'country-sl',
             'country-sg', 'country-sk', 'country-si', 'country-sb', 'country-so', 'country-za', 'country-kr',
             'country-es', 'country-lk', 'country-sd', 'country-sr', 'country-sz', 'country-se', 'country-ch',
             'country-sy', 'country-tw', 'country-tj', 'country-tz', 'country-th', 'country-bs', 'country-gm',
             'country-tl', 'country-tg', 'country-tk', 'country-to', 'country-tt', 'country-tn', 'country-tr',
             'country-tm', 'country-tc', 'country-tv', 'country-ug', 'country-ua', 'country-ae', 'country-gb',
             'country-us', 'country-uy', 'country-vi', 'country-uz', 'country-vu', 'country-va', 'country-ve',
             'country-vn', 'country-wf', 'country-ye', 'country-zm']


def get_ip(raw_ip):
    try:
        res = re.search(r'\d+\.\d+\.\d+\.\d+',raw_ip)
        if res:
            return res.group()
        split_param = re.findall(r'\(([0-9]*)\)', raw_ip)[0]
        ip_first_part = re.findall(r".write\('([0-9\.]*)'", raw_ip)[0]
        ip_second_part = re.findall(r"\+ '([0-9\.]*)'\)", raw_ip)[0]
        return ip_first_part[8:] + ip_second_part
    except:
        return None


class Proxy_list_proxynova:
    """
    proxy list from https://www.proxynova.com/proxy-server-list/
    """

    def get_proxy_list(self, limit=-1, anonymous=True, https=True, google=False, country=None):
        """
        get proxy list from "https://www.proxynova.com/proxy-server-list/"

        [params]:

        :limit: Count of proxies to return, default is -1
        """

        elite_url = "https://www.proxynova.com/proxy-server-list/elite-proxies/"
        anonymous_url = "https://www.proxynova.com/proxy-server-list/anonymous-proxies/"
        url = 'https://www.proxynova.com/proxy-server-list/'
        proxy_dicts = self.scrape_proxies(url)
        #proxy_dicts = []
        # for country in tqdm(countries):
        #     proxy_dicts += self.scrape_proxies(url + country)
        #     print(len(proxy_dicts))

        proxy_dicts += self.scrape_proxies(elite_url)
        proxy_dicts += self.scrape_proxies(anonymous_url)
        proxy_dicts = list({p['proxy_string']: p for p in proxy_dicts}.values())
        return proxy_dicts

    def scrape_proxies(self, url):
        proxy_dicts = []
        try:
            response = requests.get(url)
            if response.status_code == 200:
                df = pd.read_html(response.content)[0]

                df = df[(df['Anonymity'] == 'Anonymous') | (df['Anonymity'] == 'Elite')]
                df.loc[:, "Proxy IP"] = df['Proxy IP'].apply(lambda x: get_ip(x))
                df['proxy_string'] = df['Proxy IP'].apply(str) + ':' + df['Proxy Port'].apply(int).apply(str)
                df = df[~df['proxy_string'].isna()]
                for _, row in df.iterrows():
                    proxy_dict = {
                        'proxy': {"https": row['proxy_string'], "http": row['proxy_string']},
                        'source': 'proxynova',
                        'proxy_string': row['proxy_string'],
                        'info': {
                            'Anonymity': row['Anonymity'],
                            'Uptime': row['Uptime'],
                            'Country': row['Proxy Country']
                        }
                    }
                    proxy_dicts.append(proxy_dict)
                return proxy_dicts
        except Exception:
            print("[ERROR] Unexpected error [ProxyNova source is not working!] : TRACEBACK \n",
                traceback.format_exc(), '\n', url)
            pass

        return proxy_dicts
