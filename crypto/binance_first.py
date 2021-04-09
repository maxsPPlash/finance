import os

from binance.client import Client
from binance.websockets import BinanceSocketManager

def btc_trade_history(msg):
    ''' define how to process incoming WebSocket messages '''
    if msg['e'] != 'error':
        print(msg['b'])
        print(msg['a'])
        print('')

def binance_demo():
    # demo acc
    api_key = 'kejxyOHGm5gXciNwpV2b2AERYvHhDOvbPKCWRCuBdlGFJyqc8nAuYfznkc9n5AFE'
    api_secret = 'KFL2BMCiCXhI154onBDE6EaDwiLOesoRRY3Y8Kbe2zXqQk5g8VzvW8nF3SweNkp0'

    client = Client(api_key, api_secret)
    client.API_URL = 'https://testnet.binance.vision/api'

    btc_price = {'error': False}

    # init and start the WebSocket
    bsm = BinanceSocketManager(client)
    conn_key = bsm.start_symbol_ticker_socket('BTCEUR', btc_trade_history)
    bsm.start()

if __name__ == '__main__':
    binance_demo()