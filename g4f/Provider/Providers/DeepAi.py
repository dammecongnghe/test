import os
import json
import random
import hashlib
import requests

from ...typing import sha256, Dict, get_type_hints
random_proxies = [
    "139.59.158.185:3128"
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
    proxy_address = '157.245.247.84'
    proxy_port = '59166'
    proxies = {
    'http': f'http://32.223.6.94:80'
}
    print(proxies)
    r = requests.post("https://api.deepai.org/make_me_a_pizza", headers=headers, files=files, stream=True, proxies=proxies)

    for chunk in r.iter_content(chunk_size=None):
        r.raise_for_status()
        yield chunk.decode()


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
