# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import statsmodels.api as sm
import numpy as np

def testyf(symbols):
    print(symbols)

    today = datetime.datetime.today().isoformat()

    tickerdata1 = yf.Ticker(symbols[0])
    tickerof1 = tickerdata1.history(interval='1h', start='2021-2-1', end=today[:10])
    data1 = tickerof1['High']

    data1 = data1.diff(periods = 1)
    data1[0] = 0

#    high1.reset_index(drop=True, inplace=True);

    tickerdata2 = yf.Ticker(symbols[1])
    tickerof2 = tickerdata2.history(interval='1h', start='2021-2-1', end=today[:10])
    data2 = tickerof2['High']

    data2 = data2.diff(periods = 1)
    data2[0] = 0

    data1_shifted = data1.shift(periods=-1, fill_value = data1[-1])
    data2_shifted = data2.shift(periods=-1, fill_value = data2[-1])

    X = np.column_stack((data1_shifted, data2, data2_shifted))

    # Add a constant
    X = sm.add_constant(X)

    model = sm.OLS(data1, X)
    results = model.fit()
    print(results.summary())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tickers_list = ["BTC-USD", "ETH-USD"]
 #   tickers_list = ["TSLA", "CSIQ"]
    testyf(tickers_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
