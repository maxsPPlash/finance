import os

from binance.client import Client
from binance.websockets import BinanceSocketManager

tickers_depend = ['VET', '']
tickers_start = ['USDT']
tickers_midle = ['ETH']

ticker_id = 0

ticker_depend = tickers_depend[ticker_id]
tickers_start = tickers_start[ticker_id]
ticker_midle = tickers_midle[ticker_id]

#ticker1 = 'ENJEUR'
#ticker2 = 'ENJBNB'
#ticker3 = 'BNBEUR'

#ticker1 = 'ENJEUR'
#ticker2 = 'ENJETH'
#ticker3 = 'ETHEUR'

# maybe
ticker1 = 'VETBNB'
ticker2 = 'VETETH'
ticker3 = 'ETHBNB'


#ticker1 = 'COTIUSDT'
#ticker2 = 'COTIBNB'
#ticker3 = 'BNBUSDT'

fee_mul = (1.0 - 0.001 / 100.0)

trade_fee = fee_mul * fee_mul * fee_mul

#ticker1 = 'TKOBUSD'
#ticker2 = 'TKOBTC'
#ticker3 = 'BTCBUSD'

#ticker1 = 'BATUSDC'
#ticker2 = 'BATETH'
#ticker3 = 'ETHUSDC'

ticker_pair1 = ticker1+ticker2
ticker_pair2 = ticker2+ticker3
ticker_pair2 = ticker3+ticker1

prices = {ticker1 : 1.0, ticker2 : 1.0, ticker3 : 1.0}
arb_order = {ticker1 : 'a', ticker2 : 'b', ticker3 : 'b'}
def check_arb():
    eur_st = 100.0
    enj =  (eur_st / prices[ticker1]) * fee_mul
    bnb = enj * prices[ticker2]
    eur_end = bnb * prices[ticker3]

    eur_end *= trade_fee

    print(f' fwd res = {eur_end}')

#    if (eur_end > eur_st):
#        (f'EUR ENJ BNB EUR arbitrage {eur_end}')

prices_inv = {ticker1: 1.0, ticker2: 1.0, ticker3: 1.0}
arb_order_inv = {ticker1: 'b', ticker2: 'a', ticker3: 'a'}
def check_arb_inv():
    eur_st = 100.0
    bnb = eur_st / prices_inv[ticker3]
    enj = bnb / prices_inv[ticker2]
    eur_end = enj * prices_inv[ticker1]

    eur_end *= trade_fee

    print(f' bwd res = {eur_end}')

#    if (eur_end > eur_st):
#        (f'EUR BNB ENJ EUR arbitrage {eur_end}')

def process_message(msg):
#    print(msg)
    d = msg['data']
    ticker = d['s']
    prices[ticker] = float(d[arb_order[ticker]])
    check_arb()

    prices_inv[ticker] = float(d[arb_order_inv[ticker]])
    check_arb_inv()

def binance_demo():
    # demo acc
    api_key = 'kejxyOHGm5gXciNwpV2b2AERYvHhDOvbPKCWRCuBdlGFJyqc8nAuYfznkc9n5AFE'
    api_secret = 'KFL2BMCiCXhI154onBDE6EaDwiLOesoRRY3Y8Kbe2zXqQk5g8VzvW8nF3SweNkp0'

    client = Client(api_key, api_secret)
    client.API_URL = 'https://testnet.binance.vision/api'

    # init and start the WebSocket
    bsm = BinanceSocketManager(client)
    scanlist_Binance = [ticker1.lower() + '@ticker', ticker2.lower() +  '@ticker', ticker3.lower() + '@ticker']

    conn_key = bsm.start_multiplex_socket(scanlist_Binance, process_message)
    bsm.start()

if __name__ == '__main__':
    binance_demo()