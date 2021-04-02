import bitmex
import requests
import json
import datetime
from coinbase.wallet.client import Client
from time import sleep

#one ticker arbitrage

def arbitrage_loop():
    tichers = [['XBTUSD', 'BTC-USD'],
               ['ETHUSD', 'ETH-USD']]

    bitmex_api_key = 'EeE092m3lwJism5mAFc4plfX'
    bitmex_api_secret = 'kgRLOsB7QOfauIyyNj5VOvPQ8ueLCuWWxwXTAI4ABcqqEMqk'

    coinbase_API_key = 'cTgYvXpaksr5fFgr'
    coinbase_API_secret = 'Css2cMN9kTjPNh2XvuHLM9HrdVcX3ty5'

    client = bitmex.bitmex(api_key=bitmex_api_key, api_secret=bitmex_api_secret)

    clientb = Client(coinbase_API_key, coinbase_API_secret)

    cur_ticker = 0
    ticker_size = len(tichers)

    while True:
        positions = client.Position.Position_get(filter=json.dumps({"symbol": tichers[cur_ticker][0]})).result()[0][0]
        bitmex_btc = {}

        bitmex_btc["markPrice"] = positions["markPrice"]
#        print('BitMex: ', bitmex_btc['markPrice'])

        coinbase_btc = clientb.get_spot_price(currency_pair=tichers[cur_ticker][1])
#        print('Coinbase: ', coinbase_btc['amount'])

        bitmex_mid = float(bitmex_btc['markPrice'])
        coinbase_mid = float(coinbase_btc['amount'])

        to_bitmex = False
        if (bitmex_mid > coinbase_mid):
            to_bitmex = True

        from_price = coinbase_mid if to_bitmex else bitmex_mid
        to_price = bitmex_mid if to_bitmex else coinbase_mid

        sleep(1)

        percent = ((to_price - from_price) * 100) / from_price

        print(tichers[cur_ticker][0] + str(percent) + (' to bitmex' if to_bitmex else ' to coinbase'))

        cur_ticker = (cur_ticker + 1) % ticker_size

        if percent < 1.5:
            print('No arbitrage possibility')
            continue

        else:
            print('ARBITRAGE TIME')
            break
        sleep(1)



if __name__ == '__main__':
    arbitrage_loop()