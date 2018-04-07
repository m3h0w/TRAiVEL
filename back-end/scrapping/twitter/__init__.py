import re, os
import geopy
from TwitterAPI import TwitterAPI
from geopy.geocoders import Nominatim

tw_api_key = os.environ['TW_API_KEY']
tw_api_key_sec = os.environ['TW_API_SEC']
tw_acc_token = os.environ['TW_ACC_TOKEN']
tw_acc_token_sec = os.environ['TW_ACC_TOKEN_SEC']

api = TwitterAPI(tw_api_key, tw_api_key_sec, tw_acc_token, tw_acc_token_sec)

max_tweets = 300
city_list = ['Copenhagen','Warsaw']
country_dic = {'Copenhagen': 'Denmark', 'London': 'England','Berlin':'Germany','Amsterdam':'Nederland','Paris':'France','Warsaw':'Poland'}
lang_dic = {'Copenhagen':'da','London':'en','Berlin':'de','Amsterdam':'nl','Paris':'fr','Warsaw':'pl'}

def lat_long(city):
  country = country_dic[city]
  loc = city+', '+country

  geolocator = Nominatim()
  location = geolocator.geocode(loc)
  return str(location.latitude)+','+str(location.longitude)

def get_lat_longs(city_list):
  loc_dict = {}
  for i in city_list:
    loc = lat_long(city)
    loc_dict[i] = loc
  return loc_dict



def transform_tweet(x):
  # delete emoticons
  x = x.encode('unicode_escape').decode('utf-8')
  
  reg = r'(\\U000.{5}[ ]*)+'
  res = re.sub(reg,'',x)
  res = res.encode('utf-8').decode('unicode_escape')
  
  # remove links
  reg = r'http.*?($| )'
  res = re.sub(reg,'',res)
  
  # remove hash and ats
  reg = r'((@|#).*?[ ]*)+'
  res = re.sub(reg,'',res)

  # remove white spaces except regular space
  res = re.sub(r'[\t\n\r\f\v]','',res)
  res = re.sub(r' +',' ',res)
  
  # Remove retweets
  res = re.sub(r'RT.*?:','',res)
  
  return res.strip()

def get_tweets_city(city):
  # get the tweets around a certain city
  # Calculate the lat lon of the city
  loc = lat_long(city)+',10km'
  language = lang_dic[city]

  num_tweets = 0
  last_tweet_id = 0
  
  tweets = []
  while len(tweets) < max_tweets:
    if last_tweet_id == 0:
      response = api.request('search/tweets', params= {'count': 100, 'lang':language, 'geocode':loc})
    else:
      response = api.request('search/tweets', params= {'count': 100, 'lang':language, 'geocode':loc, 'max_id': last_tweet_id})
      
    resp_tweets = response.json()['statuses']
    
    for tweet in resp_tweets:
      text = tweet['text']
      text = transform_tweet(text)

      tweets.append(text)
  
    last_tweet = resp_tweets[-1]
    last_tweet_id = last_tweet['id']
  return tweets

def get_all_tweets(city_list):
  ret_tweets = {}
  for city in city_list:
    ret_tweets[city] = get_tweets_city(city)
  
  return ret_tweets
  

print(get_all_tweets(city_list))