from binance.client import Client
import pandas as pd
import trader


class Backtracker:
    def __init__(self, binance_client, tickers):
        client = binance_client
        self.pointers = {}
        self.data = {}
        for ticker in tickers:
            self.pointers[ticker] = 0
            bars = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1MINUTE, "3 day ago UTC")
            for line in bars:
                ticker_info = trader.TickerInfo(float(line[2]), float(line[3]), float(line[5]), int(line[8]))
                if ticker not in self.data:
                    self.data[ticker] = []
                self.data[ticker].append(ticker_info)

    def get_info(self, ticker):
        if len(self.data[ticker]) <= self.pointers[ticker]:
            return None
        result = self.data[ticker][self.pointers[ticker]]
        self.pointers[ticker] += 1
        return result