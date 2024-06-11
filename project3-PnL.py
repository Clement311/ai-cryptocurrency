import pandas as pd

file_path = 'ai-crypto-project-3-live-btc-krw.csv'
df = pd.read_csv(file_path, parse_dates=['timestamp'])

df['calculated_amount'] = df['quantity'] * df['price']

# For buys (side == 0), PnL is calculated as -(quantity * price + fee)
# For sells (side == 1), PnL is calculated as (quantity * price - fee)
df['PnL'] = df.apply(lambda row: -(row['calculated_amount']+row['fee']) if row['side'] == 0 else (row['calculated_amount']-row['fee']), axis=1)

df['cumulative_PnL'] = df['PnL'].cumsum()
df['current_quantity'] = df.apply(lambda row: row['quantity'] if row['side'] == 0 else -row['quantity'], axis=1)
df['current_quantity'] = df['current_quantity'].cumsum()
result_df = df[['timestamp','side','price','quantity','calculated_amount','fee', 'PnL', 'cumulative_PnL', ‘current_quantity']]
print(result_df)
result_df.to_csv('PnL_output.csv', index=False, sep= '|')
