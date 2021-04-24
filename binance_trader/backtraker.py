from binance.client import Client
import pandas as pd

class TickerInfo:
    def __init__(self, h, l, v, n):
        self.high = h
        self.low = l
        self.vol = v
        self.num_trades = n

class Backtracker:
    def __init__(self, binance_client, tickers):
        client = binance_client
        for ticker in tickers:
            self.pointres[ticker] = 0
            bars = client.get_historical_klines(ticker, Client.KLINE_INTERVAL_1HOUR, "30 day ago UTC")
            for line in bars:
                ticker_info = TickerInfo(float(line[2]), float(line[3]), float(line[5]), int(line[8]))
                self.data[ticker].append(ticker_info)

    def get_info(self, ticker):
        if len(self.data[ticker]) <= self.pointres[ticker]:
            return None
        result = self.data[ticker][self.pointres[ticker]]
        self.pointres[ticker] += 1
        return result