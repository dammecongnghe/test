from flask import Flask, jsonify, request
from freeGPT import AsyncClient
from asyncio import run
from flask_cors import CORS
import sys
sys.path.append('c:/python37/lib/site-packages')
import random
app = Flask(__name__)
CORS(app)
@app.route('/recommend', methods=['POST'])
async def main():

    #data = request.get_json()
    data = request.get_json()
    prompt = data['searchTerm']
    print(prompt)
    '''
    try:
        resp = await AsyncClient.create_completion("gpt4", prompt)
        print(f"🤖: {resp}")
        return jsonify(resp), 200
    except Exception as e:
        print(f"🤖: {e}")
    '''

    '''
    import requests

    url = 'https://deepsearch.mycelebs.com/api/finder/voice/maimovie'
    headers = {
    'authority': 'deepsearch.mycelebs.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/json',
    'cookie': 'first_user=true; first_result_user=true',
    'origin': 'https://deepsearch.mycelebs.com',
    'referer': 'https://deepsearch.mycelebs.com/movie',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    data = {
    'voice_content': prompt,
    'voice_lang': 'en',
    'voice_os': 'web-deepsearch',
    'voice_service': 'maimovie'
    }

    response = requests.post(url, headers=headers, json=data)
    print(response.json())
    test = response.json()['keytalks']

    url = 'https://deepsearch.mycelebs.com/api/finder/maimovie'
    headers = {
    'authority': 'deepsearch.mycelebs.com',
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.5',
    'content-type': 'application/json',
    'cookie': 'first_user=true; first_result_user=true',
    'origin': 'https://deepsearch.mycelebs.com',
    'referer': 'https://deepsearch.mycelebs.com/movie',
    'sec-ch-ua': '"Brave";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'sec-gpc': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }
    data = {
    'start': 0,
    'rows': 10,
    'keytalk': test
    }

    response = requests.post(url, headers=headers, json=data)
    '''
    import requests

    url = 'https://guessmymovie.com/submit_description?droopy=true&showad=true'
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi,zh-CN;q=0.9,zh;q=0.8,en;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'HX-Current-URL': 'https://guessmymovie.com/',
        'HX-Request': 'true',
        'Origin': 'https://guessmymovie.com',
        'Referer': 'https://guessmymovie.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    cookies = {
        'session': 'eyJ1c2VyX2lkIjogIjVlMmM1YTk1LWY1NmUtNDU4ZS04MTAxLWRjNGQ5ZDc2MDZiOSJ9.aE0OSw.3Gy5QM2DXkag0hWc15_6hT-oVTY'
    }
    
    data = {
        'description': 'movie similar spider man'
    }
    
    response = requests.post(url, headers=headers, cookies=cookies, data=data)
    
    print(response.text)
    import requests
    from bs4 import BeautifulSoup
    url = 'https://guessmymovie.com/poll?droopy=true'
    
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'vi,zh-CN;q=0.9,zh;q=0.8,en;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'HX-Current-URL': 'https://guessmymovie.com/',
        'HX-Request': 'true',
        'Referer': 'https://guessmymovie.com/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0',
        'sec-ch-ua': '"Microsoft Edge";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }
    
    cookies = {
        'session': 'eyJ1c2VyX2lkIjogIjVlMmM1YTk1LWY1NmUtNDU4ZS04MTAxLWRjNGQ5ZDc2MDZiOSJ9.aE0OVQ.6or-K7iLHyLHv71H6ygDzjvQkv4'
    }
    
    response = requests.get(url, headers=headers, cookies=cookies)
    print('split')
    print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the <a> tag with href that starts with /results/
    link_tag = soup.find('a', href=lambda x: x and x.startswith('/results/'))
    
    if link_tag:
        full_url = 'https://guessmymovie.com' + link_tag['href']
        return jsonify({'result_url': full_url}), 200
    else:
        return jsonify({'error': 'Result link not found'}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
