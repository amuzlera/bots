import config
from binance.client import Client

import mplfinance as mpf
import pandas as pd
import numpy as np

Crypto = "ETHUSDT"

client = Client(config.API_KEY, config.API_SECRET)
klines = client.get_historical_klines(Crypto, Client.KLINE_INTERVAL_4HOUR, "15 day ago UTC")

df = pd.DataFrame(klines,  columns=['Date',
                                    'Open',
                                    'High',
                                    'Low',
                                    'Close',
                                    'Volume',
                                    'Close time',
                                    'Quote asset volume',
                                    'Number of trades',
                                    'Taker buy base asset volume',
                                    'Taker buy quote asset volume',
                                    'Ignore'])

df = df.drop(df.columns[[6, 7, 8, 9, 10, 11]], axis=1)
df['Date'] = pd.to_datetime(df['Date'], unit='ms')
df.set_index('Date', inplace=True, drop=True)

df['Open']   = df['Open'].astype(float)
df['High']   = df['High'].astype(float)
df['Low']    = df['Low'].astype(float)
df['Close']  = df['Close'].astype(float)
df['Volume'] = df['Volume'].astype(float)

mpf.plot(df, type='candle', style='binance', volume=True)