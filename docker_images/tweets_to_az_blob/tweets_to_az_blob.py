#!/usr/bin/env python

from sys import prefix
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import tweepy
import pandas as pd
import numpy  as np
import nltk
import uuid
import os
import io

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

def dump_to_az_blob(csv_buf, container, connect_str):
    blob_service_client = BlobServiceClient.from_connection_string(connect_str)
    container_client = blob_service_client.get_container_client(container)
    csv_name = str(uuid.uuid4())
    blob_client = blob_service_client.get_blob_client(container, csv_name)
    blob_client.upload_blob(io.BytesIO(csv_buf), overwrite = True)

def main():
    tweets = get_tweets(os.environ['BEARER_TOKEN'], os.environ['TWITTER_QUERY'])
    df = build_tweet_dataframe(tweets)
    chunks = len(df)/int(os.environ['MAX_TABLE_SIZE'])
    df_split = np.array_split(df, chunks)
    for d in df_split:
        to_csv = d.to_csv(index=False, header=False)
        dump_to_az_blob(str.encode(to_csv), os.environ['CONTAINER'], os.environ['AZURE_CONNECT_STR'])

if __name__ == "__main__":
    main()