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

    return response.json(), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
