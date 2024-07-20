from __init__ import supplies, engine
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request

def injestdata_supplies():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(supplies, context=ssl_context) as response:
        df_iter_supplies = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_supplies = True
        records = 0

        while doing_supplies == True:
            try:
                t_start = time()
                df_supplies = next(df_iter_supplies)
                df_supplies = df_supplies.drop(['sku'], axis = 1)
                df_supplies.drop_duplicates(inplace=True)
                records += len(df_supplies)
                df_supplies.to_sql(name = 'supplies',con=engine,if_exists='append', index=False,method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_supplies = False
                print("Ingestion complete")


injestdata_supplies()
