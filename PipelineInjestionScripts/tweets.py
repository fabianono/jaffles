from __init__ import engine, tweets
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request


def injestdata_tweets():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(tweets, context=ssl_context) as response:
        df_iter_tweets = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_tweets = True
        records = 0

        while doing_tweets == True:
            try:
                t_start = time()
                df_tweets = next(df_iter_tweets)
                df_tweets['tweeted_at'] = pd.to_datetime(df_tweets['tweeted_at'])
                df_tweets.rename(columns={'user_id':'customerid'}, inplace=True)
                records += len(df_tweets)
                df_tweets.to_sql(name = 'tweets',con=engine,if_exists='append', index=False,method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_tweets = False
                print("Ingestion complete")


injestdata_tweets()
