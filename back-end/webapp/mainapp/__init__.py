# Import flask and template operators
from flask import Flask
from flask import jsonify, request

app = Flask(__name__, static_url_path='/static')

@app.route("/get_data", methods=['GET'])
def display_sentiment():
  import json
  from pprint import pprint

  data = json.load(open('data.json'))

  pprint(data)

  return jsonify(get_sentiment_list(strings_list))
