# Import flask and template operators
from flask import Flask
from flask import jsonify, request

from prices import get_prices_from_cities

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
# app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
print("CORS ADDED")

@app.route("/get_prices", methods=['POST'])
def test():
  if 'cities_list' in request.json and isinstance(request.json['cities_list'], list):
    strings_list = request.json['cities_list']
  
  month = "2018-04"
  if 'month' in request.json and isinstance(request.json['month'], str):
    month = request.json['month']

  return jsonify(get_prices_from_cities(strings_list, start_month=month, end_month=month))
