from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
import requests

def get_sentiment_list(sentences):
  sa = SentimentIntensityAnalyzer()
  sentiments = []
  for sentence in sentences:
      sentiment = sa.polarity_scores(sentence)['compound']
      sentiments.append(sentiment)
  return sentiments


def get_language_list(sentence_list):
  subscription_key = "e89813784a284b668187a0daf7c73e16"
  assert subscription_key

  text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
  
  language_api_url = text_analytics_base_url + "languages"
  print(language_api_url)

  # documents = { 'documents': [
  #   { 'id': '1', 'text': 'This is a document written in English.' },
  #   { 'id': '2', 'text': 'Este es un document escrito en Español.' },
  #   { 'id': '3', 'text': '这是一个用中文写的文件' }
  # ]}

  dict_list = [{'id': str(index+1), 'text': s} for index, s in enumerate(sentence_list)]
  documents = {'documents': dict_list}

  # response = {'documents': [{'detectedLanguages': [{'iso6391Name': 'en',
  #                                      'name': 'English',
  #                                      'score': 1.0}],
  #               'id': '1'},
  #              {'detectedLanguages': [{'iso6391Name': 'es',
  #                                      'name': 'Spanish',
  #                                      'score': 1.0}],
  #               'id': '2'},
  #              {'detectedLanguages': [{'iso6391Name': 'zh_chs',
  #                                      'name': 'Chinese_Simplified',
  #                                      'score': 1.0}],
  #               'id': '3'}],
  #   'errors': []}

  headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
  response  = requests.post(language_api_url, headers=headers, json=documents)
  response = response.json()

  languages = parseAzureResponseToList(response)
  
  from pprint import pprint
  return languages

def parseAzureResponseToList(response):
  responses = response['documents']
  return [el['detectedLanguages'][0]['iso6391Name'] for el in responses ]

def get_sentiment_list_from_azure(sentence_list,language=None):
  if language:
    assert(isinstance(language, str))

  subscription_key = "e89813784a284b668187a0daf7c73e16"
  assert subscription_key

  text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
  
  sentiment_api_url = text_analytics_base_url + "sentiment"
  print(sentiment_api_url)

  if not language:
    language_list = get_language_list(sentence_list)
  else:
    language_list = [language] * len(sentence_list)

  documents = {'documents' : [
    {'id': '1', 'language': 'en', 'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'},
    {'id': '2', 'language': 'en', 'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'},  
    {'id': '3', 'language': 'es', 'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'},  
    {'id': '4', 'language': 'es', 'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
  ]}

  documents = {'documents':[]}
  for i in range(len(sentence_list)):
    documents['documents'].append({'id':str(i+1),'language':language_list[i],'text':sentence_list[i]})


  # import requests
  from pprint import pprint

  headers   = {"Ocp-Apim-Subscription-Key": subscription_key}
  response  = requests.post(sentiment_api_url, headers=headers, json=documents)
  sentiments = response.json()
  sentiment_list = [sent['score'] for sent in sentiments['documents']]

  print(sentiment_list)


sent = ['This is great, I am so happy','omg, life sucks so much']

#get_language_from_azure(sent)
get_sentiment_list_from_azure(sent,'en')