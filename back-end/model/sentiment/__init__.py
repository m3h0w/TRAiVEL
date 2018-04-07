from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np

def get_sentiment_list(sentences):
  sa = SentimentIntensityAnalyzer()
  sentiments = []
  for sentence in sentences:
      sentiment = sa.polarity_scores(sentence)['compound']
      sentiment = int(np.round(sentiment))
      sentiments.append(sentiment)
  return sentiments
