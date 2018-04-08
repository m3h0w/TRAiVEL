# Import flask and template operators
from flask import Flask
from flask import jsonify, request

import requests

import json
import numpy as np

from flask_cors import CORS

from geopy.geocoders import Nominatim
# from requests import async

app = Flask(__name__, static_url_path='/static')
CORS(app)

def lat_long(city):
  country = country_dic[city]
  loc = city+', '+country

  geolocator = Nominatim()
  location = geolocator.geocode(loc)
  return {"latitude": location.latitude, "longitude": location.longitude}

def get_lat_longs(city_list):
  loc_dict = {}
  for i in city_list:
    loc = lat_long(city)
    loc_dict[i] = loc
  return loc_dict

country_dic = {'Copenhagen': 'Denmark', 'London': 'England','Berlin':'Germany','Amsterdam':'Nederland','Paris':'France','Warsaw':'Poland', 'Moscow': 'Russia'}
lang_dic = {'Copenhagen':'da','London':'en','Berlin':'de','Amsterdam':'nl','Paris':'fr','Warsaw':'pl', 'Russia':'ru'}

@app.route("/get_data", methods=['GET'])
def get_data():
  cities = ['Paris','Berlin','Warsaw','London']
  countries = ['FRA', 'DEU', 'POL', 'GBR']
  # countries = ["POL", "ESP"]
  sentiments = get_sentiment(cities)
  flights_raw = get_flights(cities)
  
  data = {}
  for index, country in enumerate(countries):
    flight = flights_raw[cities[index]]
    data[country] = {
      "city": cities[index], 
      "sentiment": sentiments[index], 
      "flight": {
        "price": flight["Price"],
        "outdate": flight["OutboundLegDepart"],
        "indate": flight["InboundLegDepart"],
        "airline": flight["InboundCarrier"]
      },
      "link": flight['url'],
      "location": lat_long(cities[index])      
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
  data = json.load(open('../scrapping/json/04-08.json', encoding='utf8'))
  lang_dic = {'Copenhagen':'da','London':'en','Berlin':'de','Amsterdam':'nl','Paris':'fr','Warsaw':'pl'}
  # print(cities)
  sentiment_array = []
  for city in cities:
    payload  = {'text_list':data[city],'language':lang_dic[city]}
    r = requests.post('http://127.0.0.1:8002/get_sentiment', json = payload)
    json_data = json.loads(r.text)
    sentiment_array.append(np.mean(json_data))
  #return [np.mean(json_data), np.mean(json_data) - 0.2]
  print(sentiment_array)
  return sentiment_array

def get_flights(cities):
  payload = {"cities_list": cities}
  r = requests.post('http://127.0.0.1:8003/get_prices', json = payload)
  json_data = json.loads(r.text)
  return json_data

# get_sentiment(['Amsterdam','Berlin','Copenhagen','Warsaw'])