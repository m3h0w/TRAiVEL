# Import flask and template operators
from flask import Flask
from flask import jsonify, request

from sentiment import get_sentiment_list_from_azure

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/get_sentiment", methods=['POST'])
def get_sentiment():
  if 'text_list' in request.json and isinstance(request.json['text_list'], list):
    strings_list = request.json['text_list']
  # strings_list = ['This is great, I am so happy','omg, life sucks so much']

  if 'language' in request.json and isinstance(request.json['language'], str):
    language = request.json['language'] 

  return jsonify(get_sentiment_list_from_azure(strings_list,language))

@app.route("/display_sentiment", methods=['GET'])
def display_sentiment():
  strings_list = ["This is nice!", "WHAT? OMG, I HATE THAT"]

  return jsonify(get_sentiment_list(strings_list))
