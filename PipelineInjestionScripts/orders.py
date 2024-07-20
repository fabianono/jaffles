import pandas as pd
from __init__ import engine, orders
from time import time
import certifi
import ssl
import urllib.request

def injestdata_orders():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(orders, context=ssl_context) as response:
        df_iter_orders = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_orders = True
        records = 0


        while doing_orders == True:
            try:
                t_start = time()
                df_orders = next(df_iter_orders)
                df_orders['ordered_at'] = pd.to_datetime(df_orders['ordered_at'])
                df_orders.drop(['tax_paid','order_total'],axis=1, inplace=True)
                df_orders.rename(columns={'store_id':'storeid','customer':'customerid'}, inplace=True)
                records += len(df_orders)
                df_orders.to_sql(name = 'orders',con=engine,if_exists='append', index=False, method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_orders = False
                print("Ingestion complete")


injestdata_orders()
