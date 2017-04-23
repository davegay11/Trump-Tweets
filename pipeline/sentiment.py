"""
Model the sentiment of tweets
"""

from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

def generate_polarities(df):
    # Create our sentiment analyzer
    sid = SentimentIntensityAnalyzer()
    tweets = list(df['text'])
    clean_tweets = list(df['clean_text'])
    polarities = []
    for tweet, clean_tweet in zip(tweets, clean_tweets):
        polarity['text'] = str(tweet)
        polarities.append(polarity)
    return polarities
