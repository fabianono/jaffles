from __init__ import products, engine
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request

def injestdata_typesofproducts():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(products, context=ssl_context) as response:
        df_iter_typesofproducts = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_typesofproducts = True
        records = 0

        while doing_typesofproducts == True:
            try:
                t_start = time()
                df_typesofproducts = next(df_iter_typesofproducts)
                df_typesofproducts.rename(columns={'type':'product_type'}, inplace=True)
                df_typesofproducts = df_typesofproducts[['product_type']]
                df_typesofproducts = df_typesofproducts.assign(id=range(1, len(df_typesofproducts) + 1))
                df_typesofproducts.drop_duplicates(inplace=True)
                records += len(df_typesofproducts)
                df_typesofproducts.to_sql(name = 'types_of_products',con=engine,if_exists='append', index=False,method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_typesofproducts = False
                print("Ingestion complete")


injestdata_typesofproducts()
