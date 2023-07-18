from flask import Flask, jsonify, request
from flask_cors import CORS
import g4f
import sys
sys.path.append('c:/python37/lib/site-packages')
app = Flask(__name__)
CORS(app)
def count_words(article):
    # Split the article into words using whitespace as the delimiter
    words = article.split()
    # Count the number of words
    word_count = len(words)
    return word_count
@app.route('/recommend', methods=['POST'])
def recommend():
    # Extract request data
    data = request.get_json()
    searchTerm = data['searchTerm']

    # Create OpenAI ChatCompletion request
    response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.DeepAi, messages=[
                                      {"role": "system", "content": "You are an assistant to help recommend movies and shows for people."},
            {"role": "user", "content": 'Movie and show names should always and only one be in quotes in all responses, answer concisely'},
            {"role": "assistant", "content": "Yes, I will do that."},
            {'role': 'user', 'content': searchTerm}])

    print(response)
    word_count = count_words(response)
    if(count_words==0):
        response = g4f.ChatCompletion.create(model='gpt-3.5-turbo', provider=g4f.Provider.EasyChat, messages=[
                                      {"role": "system", "content": "You are an assistant to help recommend movies and shows for people."},
            {"role": "user", "content": 'Movie and show names should always and only one be in quotes in all responses, answer concisely'},
            {"role": "assistant", "content": "Yes, I will do that."},
            {'role': 'user', 'content': searchTerm}])
        if(count_words==0):
            return jsonify(response), 429
        return jsonify(response), 200
    if(count_words==0):
        return jsonify(response), 429
    return jsonify(response), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)