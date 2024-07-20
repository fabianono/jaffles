from __init__ import products, engine
import pandas as pd
from time import time
import certifi
import ssl
import urllib.request


def injestdata_producttypes():
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(products, context=ssl_context) as response:
        df_iter_producttypes = pd.read_csv(response,iterator=True,chunksize=10000)
        doing_producttypes = True
        records = 0
        query_typesofproducts = 'select * from types_of_products'
        df_typesofproducts = pd.read_sql(query_typesofproducts,engine)

        while doing_producttypes == True:
            try:
                t_start = time()
                df_producttypes = next(df_iter_producttypes)
                df_producttypes = pd.merge(df_producttypes, df_typesofproducts, left_on='type', right_on='product_type',how = 'inner')
                df_producttypes = df_producttypes[['id','sku']]
                df_producttypes.rename(columns={'id':'types_of_productsid','sku':'productid'}, inplace=True)
                df_producttypes = df_producttypes.assign(id=range(1,len(df_producttypes)+1))
                df_producttypes.drop_duplicates(inplace=True)
                records += len(df_producttypes)
                df_producttypes.to_sql(name = 'product_types',con=engine,if_exists='append', index=False,method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except pd.errors.ParserError as e:
                print(f"Error parsing chunk: {e}")
            except StopIteration:
                doing_producttypes = False
                print("Ingestion complete")


injestdata_producttypes()
