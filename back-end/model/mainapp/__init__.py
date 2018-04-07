# Import flask and template operators
from flask import Flask
from flask import jsonify, request

from sentiment import get_sentiment

app = Flask(__name__, static_url_path='/static')

@app.route("/get_sentiment", methods=['GET'])
def test():
    # if 'text_list' in request.json and isinstance(request.json['text_list'], list):
    #   strings_list = request.json['text_list']
    strings_list = ['This is great, I am so happy','omg, life sucks so much']

    return jsonify(get_sentiment(strings_list))