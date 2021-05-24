import config
from binance.client import Client

import matplotlib.animation as animation
import mplfinance as mpf
import pandas as pd
import numpy as np


client = Client(config.API_KEY, config.API_SECRET)
crypto = 'ETHUSDT'
kline_interval = Client.KLINE_INTERVAL_1MINUTE

klines = client.get_historical_klines(crypto, kline_interval, "1 hour ago UTC")

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

pkwargs=dict(type='candle', style='binance')
fig, axes = mpf.plot(df, title='{} Price in Binance'.format(crypto), volume=True, returnfig=True, **pkwargs)

ax1 = axes[0]
ax2 = axes[2]

def animate(ival):

    candle = client.get_klines(symbol=crypto, interval=kline_interval, limit=1)

    c_open  = float(candle[0][1])
    c_high  = float(candle[0][2])
    c_low   = float(candle[0][3])
    c_close = float(candle[0][4])
    c_vol   = float(candle[0][5])
    
    df2 = pd.DataFrame({'Date':[candle[0][0]], 'Open':[c_open],'High':[c_high],'Low':[c_low],'Close':[c_close],'Volume':[c_vol]})
    df2['Date'] = pd.to_datetime(df2['Date'], unit='ms')
    df2.set_index('Date', inplace=True, drop=True)

    global df

    if df.last_valid_index() != df2.last_valid_index():
        data = pd.concat([df.iloc[1:], df2], ignore_index = False) 
        df = data
    else:
        data = df    
        data.iloc[-1, data.columns.get_loc('Open')]   = c_open
        data.iloc[-1, data.columns.get_loc('High')]   = c_high
        data.iloc[-1, data.columns.get_loc('Low')]    = c_low
        data.iloc[-1, data.columns.get_loc('Close')]  = c_close
        data.iloc[-1, data.columns.get_loc('Volume')] = c_vol
    
    ax1.clear()
    ax2.clear()

    mpf.plot(data, ax=ax1,volume=ax2,**pkwargs)

ani = animation.FuncAnimation(fig, animate, interval=250)

mpf.show()