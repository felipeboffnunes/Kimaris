from random import randint
# External Libraries
from scholarly import scholarly
from fp.fp import FreeProxy
from proxyscrape import create_collector, get_collector

def make_collector(page_i=''):
        http_collector = create_collector(f'http-collector-{page_i}', 'https')
        return http_collector

# Returns requests session with proxies (http, https)
def setup_new_proxies(http_collector):    
    proxy_http = http_collector.get_proxy()
    proxy_https = http_collector.get_proxy({'type':'https'})
    proxies={
        'http': f'http://{proxy_http.host}:{proxy_http.port}',
        'https' : f'https://{proxy_https.host}:{proxy_https.port}'
    }
    return proxies

try:
    http_collector = make_collector()
except:
    pass

def set_new_proxy():
    global http_collector
    while True:
        n = randint(0,1)
        if n == 1:
            proxy = FreeProxy(rand=True, timeout=5).get()
            print("Trying proxy:", proxy)
            if proxy == None:
                http = setup_new_proxies(http_collector)
                print("Trying proxy:", http["https"], http["https"])
                proxy_works = scholarly.use_proxy(http=http["http"], https=http["https"])
            else:
                proxy_works = scholarly.use_proxy(http=proxy, https=proxy)
        else:
            http = setup_new_proxies(http_collector)
            print("Trying proxy:", http["https"], http["https"])
            proxy_works = scholarly.use_proxy(http=http["http"], https=http["https"])
        if proxy_works:
            break
    print("Working proxy:", http["http"], http["https"])
    return http["https"]




def do_search(search_string, type=0, n=10):
    set_new_proxy()
    while True:
        try:
            search_ = scholarly.search_pubs(search_string)
            break
        except:
            set_new_proxy()
    articles = []
    for _ in range(n):
        try:
            article = next(search_)
            articles.append(article)
            print(article)
        except:
            pass
    
    return articles