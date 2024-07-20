import pandas as pd
import sqlalchemy as sa
from time import time
import certifi
import ssl
import urllib.request

engine = sa.create_engine("postgresql+psycopg2://postgres:password@104.197.193.211:5432/postgres")
#check if engine is connected and running
print(engine.connect())


#urls of csv files
customers = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_customers.csv"
items = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_items.csv"
orders = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_orders.csv"
products = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_products.csv"
stores = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_stores.csv"
supplies = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_supplies.csv"
tweets = "https://raw.githubusercontent.com/fabianono/jaffles/main/jaffle-rawdata-threeyears/threeyears_tweets.csv"


#data inspection
def inspectdata(fileurl,filename):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(fileurl, context=ssl_context) as response:
        df = pd.read_csv(response)
        #Check if ids in each file are unique. I do this because I know all of the first columns are 
        # ids but i understand that it is not always the case
        print(filename)
        if len(df[df.columns[0]].unique()) == len(df[df.columns[0]]):
            print('Id is unique')
        else:
            print('Id is not unique')
        print(pd.io.sql.get_schema(df, 'postgres', con=engine))
        print(df.head(10))
        print(f"----end of {filename} data inspection----\n")


#finding max length of long strings to determine max char limit of table
def attribute_maxstring(fileurl,columnname):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(fileurl, context=ssl_context) as response:
        df = pd.read_csv(response)
        max_chars = df[columnname].str.len().max()
        print(f"Max characters for {columnname}: {max_chars}")


#function to injest data that do not need manipulation
def injestdata(fileurl, tablename):
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    with urllib.request.urlopen(fileurl, context=ssl_context) as response:   
        df_iter = pd.read_csv(response,iterator=True,chunksize=10000)
        doing = True
        records = 0

        while doing == True:
            try:
                t_start = time()
                df = next(df_iter)
                records += len(df)
                df.to_sql(name = tablename,con=engine,if_exists='append', index=False, method='multi')
                t_end = time()
                print(f"inserted chunk, took %.5f sec, currently at {records} records"%(t_end-t_start))
            except:
                doing = False
                print("Injestion end")



#inspect table here at initialization stage to determine what data needs manipulation
if __name__ == "__main__":
    inspectdata(customers,"Customers")
    inspectdata(items,"Items")
    inspectdata(orders,"Orders")
    inspectdata(products,"Products")
    inspectdata(stores,"Stores")
    inspectdata(supplies,"Supplies")
    inspectdata(tweets,"Tweets")

