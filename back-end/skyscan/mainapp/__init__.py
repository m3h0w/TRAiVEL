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
  if 'text_list' in request.json and isinstance(request.json['text_list'], list):
    strings_list = request.json['text_list']

  return jsonify(get_prices_from_cities(strings_list))

