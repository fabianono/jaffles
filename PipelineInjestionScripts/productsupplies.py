from __init__ import supplies, engine
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request

def injestdata_productsupplies():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(supplies, context=ssl_context) as response:
        df_iter_productsupplies = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_productsupplies = True
        records = 0

        while doing_productsupplies == True:
            try:
                t_start = time()
                df_productsupplies = next(df_iter_productsupplies)
                df_productsupplies.rename(columns={'id':'supplyid','sku':'productid'}, inplace=True)
                df_productsupplies = df_productsupplies[['supplyid','productid']]
                df_productsupplies = df_productsupplies.assign(id=range(1, len(df_productsupplies) + 1))
                df_productsupplies.drop_duplicates(inplace=True)
                records += len(df_productsupplies)
                df_productsupplies.to_sql(name = 'product_supplies',con=engine,if_exists='append', index=False, method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_productsupplies = False
                print("Ingestion complete")


injestdata_productsupplies()
