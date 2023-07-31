import os
import json
import random
import hashlib
import requests

from ...typing import sha256, Dict, get_type_hints
random_proxies = [
    "103.74.121.88:3128",
    "134.209.211.64:80",
    "75.89.101.60:80",
    "75.89.101.63:80",
    "187.173.218.114:80",
    "204.157.241.12:999",
    "51.159.115.233:3128",
    "186.148.175.2:999",
    "51.254.121.123:8088",
    "82.165.32.41:80",
    "37.120.189.106:80",
    "51.38.191.151:80",
    "54.36.26.122:80",
    "38.111.111.39:80",
    "107.189.7.209:3128",
    "217.160.157.65:80",
    "81.250.223.126:80",
    "51.38.230.146:443",
    "176.31.129.223:8080",
    "91.189.177.186:3128",
    "34.125.38.1:80",
    "38.7.218.42:80",
    "179.51.179.24:8080",
    "91.65.94.145:80",
    "202.61.192.193:80",
    "189.164.248.10:80",
    "62.162.91.205:80",
    "129.153.107.221:80",
    "188.215.245.235:80",
    "162.241.207.217:80",
    "50.116.41.119:3128",
    "167.172.173.210:42847",
    "200.29.237.154:999",
    "82.65.202.229:80",
    "132.145.57.78:80",
    "220.67.2.2:80",
    "47.74.152.29:8888",
    "34.87.103.220:80",
    "72.170.220.17:8080",
    "35.240.156.235:8080",
    "124.123.108.15:80",
    "47.56.110.204:8989",
    "190.61.88.147:8080",
    "103.197.251.202:80",
    "181.65.139.232:999",
    "80.179.140.189:80",
    "91.209.11.131:80",
    "210.230.238.153:443",
    "74.82.50.155:3128",
    "82.165.184.53:80",
    "123.205.24.240:8197",
    "103.58.73.25:80",
    "41.65.103.5:1976",
    "146.59.199.12:80",
    "141.148.63.29:80",
    "164.52.221.215:80",
    "172.232.49.180:3128",
    "43.251.119.130:45787",
    "190.194.151.37:8080",
    "193.138.178.6:8282",
    "199.243.245.94:3128",
    "108.143.124.3:3128",
    "163.53.82.195:32650",
    "190.97.240.10:1994",
    "103.83.232.122:80",
    "198.44.162.6:45787",
    "216.137.184.253:80",
    "20.198.96.26:80",
    "154.65.39.7:80",
    "192.46.230.135:3128",
    # Add the rest of the proxies here...
    # Make sure the list is complete with all the proxies you provided
]
url = 'https://deepai.org'
model = ['gpt-3.5-turbo']
supports_stream = True
needs_auth = False
working = True


def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    def md5(text: str) -> str:
        return hashlib.md5(text.encode()).hexdigest()[::-1]


    def get_api_key(user_agent: str) -> str:
        part1 = str(random.randint(0, 10**11))
        part2 = md5(user_agent + md5(user_agent + md5(user_agent + part1 + "x")))
        
        return f"tryit-{part1}-{part2}"

    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'

    headers = {
        "api-key": get_api_key(user_agent),
        "user-agent": user_agent
    }

    files = {
        "chat_style": (None, "chat"),
        "chatHistory": (None, json.dumps(messages))
    }
    random_proxy = random.choice(random_proxies)
    proxies = {
    'http': 'http://' + random_proxy,
    
    }
    print(proxies)
    r = requests.post("https://api.deepai.org/chat_response", headers=headers, files=files, stream=True, proxies=proxies)

    for chunk in r.iter_content(chunk_size=None):
        r.raise_for_status()
        yield chunk.decode()


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
