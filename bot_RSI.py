import config
import websocket, json, pprint, numpy
import talib
from binance.client import Client
from binance.enums import *

SOCKET = "wss://stream.binance.com:9443/ws/ethusdt@kline_1m"
client = Client(config.API_KEY, config.API_SECRET)

def order(side, quantity, symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print("Sending order")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
        print(order)
    except Exception as e:
        print(e)
    return True


RSI_PERIOD = 14
RSI_OVERBOUHGT = 70
RSI_OVERSOLD = 30
TRADE_SYMBOL = "ETHUSDT"
TRADE_QUANTITY = 0.05
closes = []
in_position = False

def on_open(ws):
    print("Openned coneccion")

def on_close(ws):
    print("Closed connection")

def on_message(ws, message):
    global closes
    print("Recieved message")
    json_message = json.loads(message)
  #  pprint.pprint(json_message)

    candle = json_message["k"]
    is_candle_close = candle["x"]
    close = candle["c"]

    if is_candle_close:
        print("candle closed at {}".format(close))
        closes.append(float(close))
        print("closes")
        print(closes)

        if len(closes) > RSI_PERIOD:
            np_closes = numpy.array(closes)
            rsi = talib.RSI(np_closes, RSI_PERIOD)
            print("all rsi calculated so far")
            print(rsi)
            last_rsi = rsi[-1]
            print("The current rsi is {}".format(last_rsi))

            if last_rsi > RSI_OVERBOUHGT:
                if in_position:
                    print("Overbought, SELL SELL SEEEEELLLL!!!!!")
                    # put binance sell logic here
                    order_succeded = order(SIDE_SELL, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_position = False
                else:
                    print("Its overbought, but you don´t own any. Nothing to do")

            if last_rsi < RSI_OVERBOUHGT:
                if in_position:
                    print("Its overvsold, but you already buy, nothing to do")
                else:
                    print("Oversold, BUY BUY BUUUUUUUY")
                    order_succeded = order(SIDE_BUY, TRADE_QUANTITY, TRADE_SYMBOL)
                    if order_succeded:
                        in_position = True

                # put binance buy logic

ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
ws.run_forever()