# Import flask and template operators
from flask import Flask
from flask import jsonify, request

from prices import get_prices_from_cities, get_next_friday_sunday

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/get_prices", methods=['POST'])
def get_prices():
  if 'cities_list' in request.json and isinstance(request.json['cities_list'], list):
    strings_list = request.json['cities_list']

  start,end = get_next_friday_sunday()
  data = get_prices_from_cities(strings_list,start,end,origin_city='Copenhagen',currency='EUR')
  
  # month = "2018-04"
  # if 'month' in request.json and isinstance(request.json['month'], str):
  #   month = request.json['month']

  return jsonify(data)
