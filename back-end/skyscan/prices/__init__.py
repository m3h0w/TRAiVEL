import requests
import numpy as np

API_KEY = 'ha476781313606041651912031584670'
HOST = 'http://partners.api.skyscanner.net/apiservices/{endpoint}'

#Api code taken from Skyscanner
def get_api(endpoint, host=HOST, **kwargs):
  fmtd_endpoint = endpoint.format(**kwargs)
  url = host.format(endpoint=fmtd_endpoint)
  response = requests.get(url)
  return response.json()

def get_airport_code_from_cities(cities):
  assert isinstance(cities,list)
  airport_codes = []
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
      print('City not found')
      return []
    for place in resp['Places']:
      code = place['PlaceId'].split('-')[0]
      if len(code) == 3:
        airport_codes += [code]
        break
  return airport_codes

def get_cheapest_flight_info(resp):
  min_price = np.inf
  min_quote_id = 0
  i = 0
  for quote,quote_id in zip(resp['Quotes'],range(len(resp['Quotes']))):
    if len(quote.get('InboundLeg','')) & len(quote.get('OutboundLeg','')):
      if quote['MinPrice'] < min_price:
        min_quote_id = quote_id
      
  cheapest_quote = resp['Quotes'][min_quote_id]
  for carrier in resp['Carriers']:
    if len(cheapest_quote['InboundLeg']['CarrierIds']):
      if carrier['CarrierId'] == cheapest_quote['InboundLeg']['CarrierIds'][0]:
        cheapest_carrier_in = carrier['Name']
    else:
      cheapest_carrier_in = 'Unknown'
      
    if len(cheapest_quote['OutboundLeg']['CarrierIds']):
      if carrier['CarrierId'] == cheapest_quote['OutboundLeg']['CarrierIds'][0]:
        cheapest_carrier_out = carrier['Name']
    else:
      cheapest_carrier_out = 'Unknown'
    
  data = {'Price':cheapest_quote['MinPrice'],
         'InboundCarrier':cheapest_carrier_in,
         'OutboundCarrier':cheapest_carrier_out,
         'InboundLegDepart':cheapest_quote['InboundLeg']['DepartureDate'],
         'OutboundLegDepart':cheapest_quote['OutboundLeg']['DepartureDate']}
  
  
  return data

def get_prices_from_cities(cities, origin_airport='CPH',start_month='2018-07',end_month='2018-07',currency='EUR'):
  airport_codes = get_airport_code_from_cities(cities)
  price_data = {}
  for dest_airport,city in zip(airport_codes,cities):
    params = {
      'country': 'UK',
      'locale': 'en-GB',
      'currency': currency,
      'apiKey': API_KEY,
      'originPlace':origin_airport,
      'destinationPlace':dest_airport,
      'outboundPartialDate':start_month,
      'inboundPartialDate':end_month
      }
    BROWSE_DATES_ENDPOINT = '/browsedates/v1.0/{country}/{currency}/{locale}/{originPlace}/{destinationPlace}/{outboundPartialDate}/{inboundPartialDate}?apiKey={apiKey}'

    resp = get_api(BROWSE_DATES_ENDPOINT, **params)

    price_data[city] = get_cheapest_flight_info(resp)
  return price_data

# get_prices_from_cities(['paris','edmonton','berlin'])