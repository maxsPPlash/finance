import bitmex
import requests
import json
import datetime
from coinbase.wallet.client import Client
from time import sleep

#one ticker arbitrage

def arbitrage_loop():
    coinbase_API_key = 'cTgYvXpaksr5fFgr'
    coinbase_API_secret = 'Css2cMN9kTjPNh2XvuHLM9HrdVcX3ty5'

    clientb = Client(coinbase_API_key, coinbase_API_secret)

    while True:
        coinbase_btceth = clientb.get_buy_price(currency_pair='ETH-USD')
#        print('Coinbase: ', coinbase_btc['amount'])
        coinbase_mid = float(coinbase_btceth['amount'])

        print(coinbase_btceth)

        sleep(1)



if __name__ == '__main__':
    arbitrage_loop()