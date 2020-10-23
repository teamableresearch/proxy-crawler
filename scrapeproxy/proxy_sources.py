from .handlers.us_proxy_org import Proxy_list_proxyorg
from .handlers.pubproxy_com import Proxy_list_pubproxy
from .handlers.proxy_list import Proxy_list_proxylist
from .handlers.proxynova import Proxy_list_proxynova
from .handlers.proxyscr import Proxy_list_proxyscrp
# ordered list of sources for proxies(with handling class) ordered by trust level
proxy_sources = [
    {
        # add the rest of us-proxy countries
        "id": "best",
        "source": "https://www.us-proxy.org/",
        "handler": Proxy_list_proxyorg,
        "trust": "normal"
    },
    {
        # limited count in free version
        "id": "pub",
        "source": "http://pubproxy.com",
        "handler": Proxy_list_pubproxy,
        "trust": "normal"
    },
    {
        "id": "proxylist",
        "source": "https://www.proxy-list.download",
        "handler": Proxy_list_proxylist,
        "trust": "normal"
    },
    {
        # need a fix
        "id": "proxynova",
        "source": "https://www.proxynova.com/proxy-server-list",
        "handler": Proxy_list_proxynova,
        "trust": "normal"
    },
    {
        # need a fix
        "id": "proxyscrp",
        "source": "https://www.proxyscrape.com/free-proxy-list",
        "handler": Proxy_list_proxyscrp,
        "trust": "normal"
    }
]
