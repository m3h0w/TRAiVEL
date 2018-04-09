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

city_list = ['Lisbon','Rome','Vienna','Zurich','Oslo','Stockholm','Helsinki','Moscow','Copenhagen','Berlin','Warsaw','Paris','London','Dublin','Amsterdam','Bruxelles','Madrid']
country_dic = {'Copenhagen':'Denmark','Berlin':'Germany','Warsaw':'Poland','Paris':'France','London':'England','Dublin':'Ireland','Amsterdam':'The Netherlands','Bruxelles':'Belgium','Madrid':'Spain','Lisbon':'Portugal','Rome':'Italie','Vienna':'Austria','Zurich':'Zwitserland','Oslo':'Norway','Stockholm':'Sweden','Helsinki':'Finland','Moscow':'Russia'}
lang_dic = {'Copenhagen':'da','Berlin':'de','Warsaw':'pl','Paris':'fr','London':'en','Dublin':'en','Amsterdam':'nl','Bruxelles':'fr','Madrid':'es','Lisbon':'pt','Rome':'it','Vienna':'de','Zurich':'de','Oslo':'no','Stockholm':'sv','Helsinki':'fi','Moscow':'ru'}

@app.route("/get_data", methods=['GET'])
def get_data():
  cities = ['Lisbon','Rome','Vienna','Zurich','Oslo','Stockholm','Helsinki','Moscow','Berlin','Warsaw','Paris','London','Dublin','Amsterdam','Bruxelles','Madrid']
  countries = ['PRT', 'ITA', 'AUT', 'CHE', 'NOR', 'SWE', 'FIN', 'RUS', 'DEU','POL', 'FRA', 'GBR', 'IRL', 'NLD', 'BEL', 'ESP']
  # countries = ["POL", "ESP"]
  sentiments = get_sentiment_from_file(cities)
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

@app.route("/get_data_madrid", methods=['GET'])
def get_data_madrid():
  cities = ['Lisbon','Rome','Vienna','Zurich','Oslo','Stockholm','Helsinki','Moscow','Berlin','Warsaw','Paris','London','Dublin','Amsterdam','Bruxelles','Madrid']
  countries = ['PRT', 'ITA', 'AUT', 'CHE', 'NOR', 'SWE', 'FIN', 'RUS', 'DEU','POL', 'FRA', 'GBR', 'IRL', 'NLD', 'BEL', 'ESP']
  # countries = ["POL", "ESP"]
  # sentiments = get_sentiment_from_file(cities)
  sentiments = [0.464172018988058, 0.5249947293065488, 0.5177478067409247, 0.5073912304509431, 0.5013169356137515, 0.5684756477922202, 0.627079818636179, 0.5072345736026764, 0.5469414733164012, 0.6184176307711751, 0.4788615402765572, 0.5168948508501053, 0.5299666111767292, 0.5673802295923233, 0.5039202862847596, 0.7503749640733004]
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

  return jsonify(data)

def get_sentiment(cities):
  data = json.load(open('../scrapping/json/2018-04-08.json', encoding='utf8'))
  # lang_dic = {'Copenhagen':'da','London':'en','Berlin':'de','Amsterdam':'nl','Paris':'fr','Warsaw':'pl'}
  # print(cities)
  sentiment_array = []
  for city in cities:
    payload  = {'text_list':data[city],'language':lang_dic[city]}
    r = requests.post('http://127.0.0.1:8002/get_sentiment', json = payload)
    json_data = json.loads(r.text)
    sentiment_array.append(np.mean(json_data))
  #return [np.mean(json_data), np.mean(json_data) - 0.2]
  with open('json/sent.json','w') as f:
    json.dump(sentiment_array,f)

  return sentiment_array

def get_sentiment_from_file(cities):
  sentiment_list = json.load(open('json/sent.json', encoding='utf8'))
  if len(sentiment_list) != len(cities):
    return get_sentiment(cities)
  
  return sentiment_list

def get_flights(cities):
  payload = {"cities_list": cities}
  r = requests.post('http://127.0.0.1:8003/get_prices', json = payload)
  json_data = json.loads(r.text)
  return json_data

# get_sentiment(['Amsterdam','Berlin','Copenhagen','Warsaw'])