# Import flask and template operators
from flask import Flask
from flask import jsonify, request
import twitter

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/get_tweets", methods=['POST'])
def get_tweets():
  if 'cities_list' in request.json and isinstance(request.json['cities_list'], list):
    strings_list = request.json['cities_list']
  
  return jsonify(get_all_tweets(strings_list))

@app.route("/get_lat_long", methods=['POST'])
def get_lat_long():
  if 'cities_list' in request.json and isinstance(request.json['cities_list'], list):
    strings_list = request.json['cities_list']
  
  return jsonify(get_lat_longs(strings_list))






