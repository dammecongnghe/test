from flask import Flask, jsonify, request
from freeGPT import Client
from asyncio import run
from flask_cors import CORS
import sys
sys.path.append('c:/python37/lib/site-packages')
import random
app = Flask(__name__)
CORS(app)
@app.route('/recommend', methods=['POST'])
def main():

    #data = request.get_json()
    data = request.get_json()
    prompt = data['searchTerm']
    print(prompt)
    try:
        resp = Client.create_completion("gpt4", prompt)
        print(f"🤖: {resp}")
        return jsonify(resp), 200
    except Exception as e:
        print(f"🤖: {e}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
