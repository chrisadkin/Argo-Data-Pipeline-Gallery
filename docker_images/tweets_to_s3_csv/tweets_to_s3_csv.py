#!/usr/bin/env python

from sys import prefix
import tweepy
import pandas as pd
import numpy  as np
import boto3
import nltk
import uuid
import os

from tweepy.tweet import Tweet
from nltk.sentiment.vader import SentimentIntensityAnalyzer

def get_tweets(bearer_token, query, max_tweets=1000):
    client = None
    tweets = None

    client = tweepy.Client(bearer_token=bearer_token)
    tweets = tweepy.Paginator(client.search_recent_tweets,
                              query,
                              max_results=100).flatten(limit=max_tweets)
    return tweets


def build_tweet_dataframe(tweets):
    tweet_list =[]
    nltk.download('vader_lexicon', quiet=True)
    for tweet in tweets:
        tweet_id = tweet.id 
        text = tweet.text 
        score = SentimentIntensityAnalyzer().polarity_scores(text)
        tweet_list.append({'tweet_id'  : tweet_id, 
                           'text'      : text, 
                           's_negative': score['neg'],
                           's_neutral' : score['neu'], 
                           's_positive': score['pos'], 
                           's_compound': score['compound']})
    # create dataframe   
    df = pd.DataFrame(tweet_list, columns=['tweet_id',
                                           'text',
                                           's_negative',
                                           's_neutral',
                                           's_positive',
                                           's_compound'])
    return df

def dump_to_s3(csv_buf, aws_endpoint, bucket, aws_key, aws_secret):
    s3 = boto3.resource(service_name          = 's3',
                        use_ssl               = False,
                        aws_access_key_id     = aws_key,
                        aws_secret_access_key = aws_secret,
                        endpoint_url          = aws_endpoint)

    csv_name = str(uuid.uuid4())
    s3.Object(os.environ['BUCKET'], csv_name).put(Body=csv_buf)

def main():
    tweets = get_tweets(os.environ['BEARER_TOKEN'], os.environ['TWITTER_QUERY'])
    df = build_tweet_dataframe(tweets)
    chunks = len(df)/int(os.environ['MAX_TABLE_SIZE'])
    df_split = np.array_split(df, chunks)
    for d in df_split:
        to_csv = d.to_csv(index=False, header=False)
        dump_to_s3(to_csv, os.environ['ENDPOINT_URL'], os.environ['BUCKET'],
                   os.environ['AWS_ACCESS_KEY_ID'], os.environ['AWS_SECRET_ACCESS_KEY'])


if __name__ == "__main__":
    main()
