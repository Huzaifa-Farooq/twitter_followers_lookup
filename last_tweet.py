import pandas as pd
import requests
import os
import time
import tweepy

access_token = '1013263399130685440-gqy1ctLoVWceR1vahSd8Dx7VpmNmzr'
access_token_secret = 'TPHWlxvETSHVas7y9unvSUi6lO5s5JWPYH0lOkD6NzRwg'
consumer_key = '0sqNDfPjWoOstQwgLIOkTJfzP'
consumer_secret = 'q5PfPWm54XCPZpoITbxc8YlmtxAvlqxdqSDBmp0UMD1QoReiDn'
BEARER_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAOapJwEAAAAAPlPvZbS6PpcjJK6qjQ79EyZDN%2BQ%3DtMmXIpSV9NSePe0NK8zoZNcnJXYGSsm8ty9IeDNcPJuhSQJ7YD'

def get_last_tweet_date(df):
    """ function to get and insert last tweet date to user's dataframe """
    usernames = list(df['username'])
    last_tweet_date = []
    for username in usernames:
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=False)
        print(username)
        tweets = api.user_timeline('ShoaibC87817172', count=10)
        for t in tweets:
            print(t._json['created_at'])
        print(tweets)
        exit()

df = pd.read_csv(f"D:\\Huzaifa\\ai\\AI\\COVID\\twitter\\MaryamNSharif\\followers\\followers0.csv")
get_last_tweet_date(df)