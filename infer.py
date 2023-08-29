from flask import Flask, jsonify, request
from freeGPT.gpt4 import Completion
from flask_cors import CORS
import g4f
import sys
sys.path.append('c:/python37/lib/site-packages')
import random

# Your existing code here...

# List of proxies
proxies = [
    "51.159.115.233:3128",
    "34.87.130.147:8080",
    "210.230.238.153:443",
    "200.143.75.194:8080",
    "172.104.97.150:32539",
    "117.251.103.186:8080",
    "150.109.12.63:8999",
    "8.209.114.72:3129",
    "20.204.190.254:3129",
    "186.121.235.66:8080",
    "193.233.202.75:8080",
    "110.34.3.229:3128",
    "5.202.53.65:8080",
    "142.93.136.183:3128",
    "103.158.121.201:8181",
    "103.53.77.189:8080",
    "129.154.225.163:8100",
    "20.44.206.138:80",
    "188.132.222.3:8080",
    "172.104.80.43:32539",
    "117.3.241.30:23777",
    "158.160.56.149:8080",
    "190.90.39.72:999",
    "172.104.97.150:32539",
    "34.87.130.153:8080",
    "103.206.246.229:8080",
    "111.224.216.237:8089",
    "23.152.40.15:3128",
    "173.82.245.139:3128",
    "37.120.192.154:8080",
    "123.126.158.50:80"
    # Add the rest of the proxies here...
    # Make sure the list is complete with all the proxies you provided
]
app = Flask(__name__)
CORS(app)
def count_words(article):
    # Split the article into words using whitespace as the delimiter
    words = article.split()
    # Count the number of words
    word_count = len(words)
    return word_count
@app.route('/recommend', methods=['POST'])
async def recommend():
    # Extract request data
    data = request.get_json()
    searchTerm = data['searchTerm']
    random_proxy = random.choice(proxies)
    prompt = 'You are an assistant to help recommend movies and shows for people. Movie and show names should always and only one be in quotes in all responses, answer concisely'
    # Create OpenAI ChatCompletion request
    prompt = prompt + searchTerm
    completion = Completion()
    
    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.You,  messages=[
                                      {"role": "system", "content": "You are an assistant to help recommend movies and shows for people."},
            {"role": "user", "content": 'Movie and show names should always and only one be in quotes in all responses, answer concisely'},
            {"role": "assistant", "content": "Yes, I will do that."},
            {'role': 'user', 'content': searchTerm}])
    '''
    response = await completion.create(prompt=prompt)
    '''
    
    print(response)
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)