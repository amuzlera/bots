import config
import websocket
import json
import pprint
import numpy as np
import talib
from binance.client import Client
from binance.enums import *

import mplfinance as mpf
import pandas as pd

client = Client(config.API_KEY, config.API_SECRET)



RSI_PERIOD = 14
RSI_OVERBOUHGT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSDT"
historial = []
lastPrice = 0
lastEth = 0
lastUsdt = 0
rendimientoBot = 0

# Con esto arrancas la simulacion
usdt = 0
eth = 0.05
tengoplata = False

klines = client.get_historical_klines(TRADE_SYMBOL, Client.KLINE_INTERVAL_1HOUR, "90 day ago UTC")
#Le da formato a la lista con las columnas como se descargan
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

closePrice  = df['Close'].astype(float)
rsi = talib.RSI(closePrice, RSI_PERIOD)

for i in range(RSI_PERIOD+1, len(closePrice)):
    if rsi[i] > RSI_OVERBOUHGT and tengoplata==False:
        # Simulacion de venta
        usdt= (eth*closePrice[i])*0.99925

        lastPrice=closePrice[i]
        lastEth = eth



        historial.append("Venta de {} eth a un precio de {} por {} usdt".format(eth, closePrice[i], usdt))
        eth=0

        tengoplata=True

        
        
    
    if rsi[i] < RSI_OVERSOLD and tengoplata:
        # Simulacion de compra
        eth = (usdt/closePrice[i])*0.99925   #Convierto mis dolares a eth al precio de mercado - la comision de Binance
        lastUsdt = usdt
        historial.append("Compra {} eth a un precio de {} por {} usdt".format(eth, closePrice[i], usdt))
        usdt=0

        tengoplata = False


pprint.pprint(historial)
lenght= len(closePrice)
usdtHold = closePrice[lenght-1]*0.05
print(usdtHold)

if tengoplata==False:
    rendimientoBot= 100*lastEth*lastPrice/usdtHold
if tengoplata:
    rendimientoBot = 100*lastUsdt/usdtHold

rendimientoBot = round(rendimientoBot, 2)

print("el rendimiento del bot fue de {}%".format(rendimientoBot))
print(df['Date'])

#print(lastUsdt)
#print(lastEth)
#print(lastPrice)
