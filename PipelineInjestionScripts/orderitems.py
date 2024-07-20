import pandas as pd
from __init__ import engine, items
from time import time
import certifi
import ssl
import urllib.request

def injestdata_orderitems():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(items, context=ssl_context) as response:
        df_iter_orderitems = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_orderitems = True
        records = 0

        while doing_orderitems == True:
            try:
                t_start = time()
                df_orderitems = next(df_iter_orderitems)
                df_orderitems.rename(columns={'order_id':'orderid','sku':'productid'}, inplace=True)
                records += len(df_orderitems)
                df_orderitems.to_sql(name = 'order_items',con=engine,if_exists='append', index=False,method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_orderitems = False
                print("Ingestion complete")


injestdata_orderitems()