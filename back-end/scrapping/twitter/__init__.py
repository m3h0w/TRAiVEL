import re, os, sys
import geopy
from TwitterAPI import TwitterAPI
from geopy.geocoders import Nominatim
import pickle
import datetime
import json

tw_api_key = os.environ['TW_API_KEY']
tw_api_key_sec = os.environ['TW_API_SEC']
tw_acc_token = os.environ['TW_ACC_TOKEN']
tw_acc_token_sec = os.environ['TW_ACC_TOKEN_SEC']

api = TwitterAPI(tw_api_key, tw_api_key_sec, tw_acc_token, tw_acc_token_sec)

max_tweets = 1000
city_list = ['Lisbon','Rome','Vienna','Zurich','Oslo','Stockholm','Helsinki','Moscow','Copenhagen','Berlin','Warsaw','Paris','London','Dublin','Amsterdam','Bruxelles','Madrid']
country_dic = {'Copenhagen':'Denmark','Berlin':'Germany','Warsaw':'Poland','Paris':'France','London':'England','Dublin':'Ireland','Amsterdam':'The Netherlands','Bruxelles':'Belgium','Madrid':'Spain','Lisbon':'Portugal','Rome':'Italie','Vienna':'Austria','Zurich':'Zwitserland','Oslo':'Norway','Stockholm':'Sweden','Helsinki':'Finland','Moscow':'Russia'}

#city_list = ['Copenhagen','Warsaw','London','Berlin','Amsterdam','Paris']
#city_list = ['London']
lang_dic = {'Copenhagen':'da','Berlin':'de','Warsaw':'pl','Paris':'fr','London':'en','Dublin':'en','Amsterdam':'nl','Bruxelles':'fr','Madrid':'es','Lisbon':'pt','Rome':'it','Vienna':'de','Zurich':'de','Oslo':'no','Stockholm':'sv','Helsinki':'fi','Moscow':'ru'}

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

def get_tweets_city(city, day):
  # get the tweets around a certain city
  # Calculate the lat lon of the city
  loc = lat_long(city)+',10km'
  language = lang_dic[city]
  upperdate = datetime.datetime.strptime(day + ' +0000', '%Y-%m-%d %z')
  num_tweets = 0
  last_tweet_id = 0
  print(city)
  tweets = []
  diff = 0
  while num_tweets < max_tweets:
    if last_tweet_id == 0:
      if day == None:
        response = api.request('search/tweets', params= {'count': 100, 'lang':language,'geocode':loc})
      else:
        response = api.request('search/tweets', params= {'count': 100, 'lang':language,'until':day,'geocode':loc})
    else:
      response = api.request('search/tweets', params= {'count': 100, 'lang':language,'geocode':loc, 'max_id': last_tweet_id})
    
    try:
      resp_tweets = response.json()['statuses']
    except:
      print(response.json())
      sys.exit(0)
      

    for tweet in resp_tweets:
      text = tweet['text']
      text = transform_tweet(text)

      tweets.append(text)

    num_tweets = len(tweets)
    last_tweet = resp_tweets[-1]
    last_tweet_id = last_tweet['id']
    last_time = datetime.datetime.strptime(last_tweet['created_at'],'%a %b %d %H:%M:%S %z %Y')
    diff = (upperdate-last_time).days
    print('Last Batch ', last_tweet['created_at'],diff)

  print('First tweet',resp_tweets[-1]['created_at'])
  return tweets

def get_all_tweets(city_list,day = None):
  json_name = 'json/'+day+'.json'
  ret_tweets = {}
  if os.path.isfile(json_name):
    ret_tweets = json.load(open(json_name,'r'))

  for city in (set(city_list)-set(ret_tweets.keys())):
    ret_tweets[city] = get_tweets_city(city,day)

    with open(json_name,'w') as f:
      json.dump(ret_tweets,f) 

  return ret_tweets

# get_all_tweets(city_list,'2018-04-08')
