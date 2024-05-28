import csv
import datetime
import pandas as pd
import os

ratio = 0.2
level = 5
interval = 1

data = pd.read_csv("2024-04-25-bithumb-ETH.csv",header=None, names=['price', 'quantity', 'type','timestamp'])
df = pd.DataFrame(data)

groups = df.groupby("timestamp")

keys = groups.groups.keys()

for i in keys:
        ask_or_bid = groups.get_group(i).groupby("type")
        bids = ask_or_bid.get_group(0).reset_index()
        asks = ask_or_bid.get_group(1).reset_index()

        mid_price = ((asks.price[0]+bids.price[0])*0.5)


        askQty = 0
        bidQty = 0
        askPx = 0
        bidPx = 0
        for j in range(5):
                askQty += pow(asks.quantity[j],ratio)
                bidQty += pow(bids.quantity[j],ratio)
                askPx += asks.price[j]*pow(asks.quantity[j],ratio)
                bidPx += bids.price[j]*pow(bids.quantity[j],ratio)
        book_price = (((askQty*bidPx)/bidQty)+((bidQty*askPx)/askQty))/(bidQty+askQty)
        book_imbalance = (book_price-mid_price)/interval

        result = {
        "book-imbalance-0.2-5-1": [book_imbalance],
        "mid_price": mid_price,
        "timestamp": i
        }
        result = pd.DataFrame(result)

        output_file = "2024-04-25-bithumb-ETH-feature.csv"
        should_write_header = not os.path.exists(output_file)
        result.to_csv(output_file, index=False, header=should_write_header, mode='a',sep='|')
