# Import flask and template operators
from flask import Flask
from flask import jsonify, request

import requests

import json
import numpy as np

from flask_cors import CORS

app = Flask(__name__, static_url_path='/static')
CORS(app)

@app.route("/get_data", methods=['GET'])
def get_data():
  cities = ["Warsaw", "Madrid"]
  countries = ["POL", "ESP"]
  sentiments = get_sentiment(cities)
  flights_raw = get_flights(cities, "2018-04")
  
  
  data = {}
  for index, country in enumerate(countries):
    flight = flights_raw[cities[index]]
    data[country] = {
      "city": cities[index], 
      "sentiment": sentiments[index], 
      "flight": {
        "price": flight["Price"],
        "data": flight["InboundLegDepart"],
        "airlineLogo": flight["InboundCarrier"] + ".png"
      }
    } 

  # print(data)

  # responseData = {
  #   "POL": {
  #     "city": "Warsaw",
  #     "sentiment": 0.5,
  #     "flight": {
  #       "price": 200,
  #       "date": "01.02.1993",
  #       "airlineLogo": "lot.png"
  #     }
  #   },
  #   "ESP": {
  #     "city": "Madrid",
  #     "sentiment": 1,
  #     "flight": {
  #       "price": 100,
  #       "date": "30.02.2018",
  #       "airlineLogo": "lot.png"
  #     }
  #   }
  # }

  return jsonify(data)

def get_sentiment(cities):
  data = json.load(open('mainapp/tweets.json', encoding="utf8"))
  the_list = [el[0] for el in data['tweets']]
  payload = {"text_list": the_list}
  r = requests.post('http://127.0.0.1:8002/get_sentiment', json = payload)
  json_data = json.loads(r.text)
  return [np.mean(json_data), np.mean(json_data) - 0.2]

def get_flights(cities, month):
  payload = {"cities_list": cities}
  r = requests.post('http://127.0.0.1:8003/get_prices', json = payload)
  json_data = json.loads(r.text)
  return json_data