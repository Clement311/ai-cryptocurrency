import time
import requests
import pandas as pd
import datetime
import os

current_date = datetime.datetime.now().date()
file_name = f"./book-{current_date}-bithumb-btc.csv"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

while(1):    
    book = {}
    response = requests.get ('https://api.bithumb.com/public/orderbook/BTC_KRW/?count=5',headers = headers)
    book = response.json()


    data = book['data']

    bids = (pd.DataFrame(data['bids'])).apply(pd.to_numeric,errors='ignore')
    bids.sort_values('price', ascending=False, inplace=True)
    bids = bids.reset_index(); del bids['index']
    bids['type'] = 0
    
    asks = (pd.DataFrame(data['asks'])).apply(pd.to_numeric,errors='ignore')
    asks.sort_values('price', ascending=True, inplace=True)
    asks['type'] = 1 

    df = bids.append(asks)
    
    timestamp = datetime.datetime.now()
    req_timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')

    df['quantity'] = df['quantity'].round(decimals=4)
    df['timestamp'] = req_timestamp
    
    print (df)
    print ("\n")

    if current_date !=datetime.datetime.now().date():
        current_date = datetime.datetime.now().date()
        file_name =f"./book-{current_date}-bithumb-btc.csv"
    
    df.to_csv(file_name, index=False, header=False, mode = 'a')
    time.sleep(4.9)
