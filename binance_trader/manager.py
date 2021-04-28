import trader
import backtraker
from binance.client import Client
import collections


class Manager:
    def __init__(self, custom_tickers=None):
        file = open('binance_info.txt')  # 1 line key 2 line secret
        bin_cred = file.read().splitlines()

        api_key = bin_cred[0]
        api_secret = bin_cred[1]

        client = Client(api_key, api_secret)

        self.tickers = {'AAVEUSDT', 'ADABUSD', 'CHZUSDT'}
        if custom_tickers is not None:
            self.tickers = custom_tickers

        self.data = backtraker.Backtracker(client, self.tickers)

        self.historical_data = {}
        for ticker in self.tickers:
            self.historical_data[ticker] = collections.deque(maxlen=100)

        self.traders = {}

        self.init_traders()

    def update(self):
        for ticker in self.tickers:
            inf = self.data.get_info(ticker)
            if inf is None:
                continue

            self.historical_data[ticker].append(inf)

            for tr in self.traders[ticker]:
                tr.update(self.historical_data[ticker])

    def init_traders(self):
        for ticker in self.tickers:
            self.traders[ticker] = []
            self.traders[ticker].append(trader.Trader(ticker, trader.BuyAlgo99cross(), trader.SellAlgoBase()))
