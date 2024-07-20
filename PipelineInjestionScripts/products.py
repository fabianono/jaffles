from __init__ import products, engine
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request


def injestdata_product():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(products, context=ssl_context) as response:
        df_iter_products = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_products = True
        records = 0

        while doing_products == True:
            try:
                t_start = time()
                df_products = next(df_iter_products)
                df_products.drop(['type'],axis=1,inplace=True)
                df_products.rename(columns={'sku':'id'}, inplace=True)
                df_products.drop_duplicates(inplace=True)
                records += len(df_products)
                df_products.to_sql(name = 'products',con=engine,if_exists='append', index=False, method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_products = False
                print("Ingestion complete")


injestdata_product()
