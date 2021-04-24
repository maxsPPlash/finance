import trader
import backtraker
from binance.client import Client

class Manager:
    def __init__(self, custom_tickers = None):
        file = open('binance_info.txt')  # 1 line key 2 line secret
        bin_cred = file.read().splitlines()

        api_key = bin_cred[0]
        api_secret = bin_cred[1]

        client = Client(api_key, api_secret)

        self.tickers = {'AAVEUSDT', 'ADABUSD', 'CHZUSDT'}
        if custom_tickers != None:
            self.tickers = custom_tickers

        self.data = backtraker.Backtracker(client, self.tickers)

    def start(self):
        for ticker in self.tickers:
            res = self.data.get_info(ticker)
            if (res != None):
                self.update(res)

    def register_data_flow(self, source):
        self.data_flow = source

    def update(self, ticker_info):
        #dosomething
        pass

    def init_traders(self):
        pass
