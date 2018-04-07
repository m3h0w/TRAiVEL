import time
import requests
import datetime
import pandas as pd
import numpy as np

API_KEY = 'ha476781313606041651912031584670'
HOST = 'http://partners.api.skyscanner.net/apiservices/{endpoint}'

#Api code taken from Skyscanner
def get_api(endpoint, host=HOST, **kwargs):
  fmtd_endpoint = endpoint.format(**kwargs)
  url = host.format(endpoint=fmtd_endpoint)
  response = requests.get(url)
  return response.json()

def get_next_friday_sunday():
  today = pd.Timestamp.now()
  if today.weekday() > 4:
    next_friday = (datetime.datetime.strptime('%s-%s-5'%(today.year,today.week),'%Y-%W-%w') + pd.DateOffset(weeks=1))
  else:
    next_friday = datetime.datetime.strptime('%s-%s-5'%(today.year,today.week),'%Y-%W-%w')
  next_sunday = next_friday + pd.DateOffset(days=2)
  return next_friday.strftime('%Y-%m-%d'), next_sunday.strftime('%Y-%m-%d')

def get_city_codes_from_cities(cities):
  assert isinstance(cities,list)
  city_codes = {}
  for city in cities:
    params = {
      'country': 'UK',
      'currency': 'GBP',
      'locale': 'en-GB',
      'query': city,
      'apiKey': API_KEY
    }

    AUTO_SUGGEST_ENDPOINT = 'autosuggest/v1.0/{country}/{currency}/{locale}/?query={query}&apiKey={apiKey}'

    resp = get_api(AUTO_SUGGEST_ENDPOINT, **params)
    if len(resp['Places']) == 0:
      print('City not found %s'%city)
    
    city_codes[city] = resp['Places'][0]['PlaceId']
        
  return city_codes


def get_cheapest_price_for_flight(origin,destination,start,end,currency='EUR'):
  assert isinstance(start,str)
  assert isinstance(end,str)
  
  params = {
  'apiKey': API_KEY,
  'country': 'UK',
  'locale': 'en-GB',
  'locationSchema': 'Sky',
  'currency': currency,
  'originPlace':origin,
  'destinationPlace':destination,
  'outboundDate':start,
  'inboundDate':end,
  'adults':1
  }
  r = requests.post('http://partners.api.skyscanner.net/apiservices/pricing/v1.0',data=params)
  response = requests.get(r.headers['Location']+'?apiKey=%s&sorttype=price&pageSize=1&pageIndex=1'%API_KEY)
  while response.status_code == 304:
    time.sleep(0.5)
    response = requests.get(r.headers['Location']+'?apiKey=%s&sorttype=price&pageSize=1&pageIndex=1'%API_KEY)
  raw = response.json()
  response.close()
  
  in_carrier_id = raw['Legs'][1]['Carriers'][0]
  out_carrier_id = raw['Legs'][0]['Carriers'][0]
  in_carrier_name = [carrier['Name'] for carrier in raw['Carriers'] if carrier['Id'] == in_carrier_id][0]
  out_carrier_name = [carrier['Name'] for carrier in raw['Carriers'] if carrier['Id'] == out_carrier_id][0]
 
  
  out = {'Price':raw['Itineraries'][0]['PricingOptions'][0]['Price'],
         'url':raw['Itineraries'][0]['PricingOptions'][0]['DeeplinkUrl'],
         'InboundCarrier':in_carrier_name,
         'OutboundCarrier':out_carrier_name,
         'InboundLegArrive':raw['Legs'][1]['Arrival'],
         'InboundLegDepart':raw['Legs'][1]['Departure'],
         'OutboundLegDepart':raw['Legs'][0]['Departure'],
         'OutboundLegArrive':raw['Legs'][0]['Arrival']}
  return out

def get_prices_from_cities(cities,start_date,end_date,origin_city='Copenhagen',currency='EUR'):
  origin_city_code = get_city_codes_from_cities([origin_city])[origin_city]
  dest_city_codes = get_city_codes_from_cities(cities)
  price_data = {}
  for dest_city,dest_city_code in dest_city_codes.items():
    price_data[dest_city] = get_cheapest_price_for_flight(origin_city_code,dest_city_code,start_date,end_date)
  return price_data

#start,end = get_next_friday_sunday()
#get_prices_from_cities(['Amsterdam','Berlin','Warsaw','Moscow'],start,end,origin_city='Copenhagen',currency='EUR')
