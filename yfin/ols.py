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
    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 9))

    today = datetime.datetime.today().isoformat()

    tickerdata1 = yf.Ticker(symbols[0])
    tickerof1 = tickerdata1.history(interval='1d', start='2019-1-1', end=today[:10])
    high1 = tickerof1['High']

    tickerdata2 = yf.Ticker(symbols[1])
    tickerof2 = tickerdata2.history(interval='1d', start='2019-1-1', end=today[:10])
    high2 = tickerof2['High']
#    high2.columns[0] = symbols[1]

    # Add a constant
    X = sm.add_constant(high2)

    model = sm.OLS(high1, X)
    results = model.fit()
    print(results.summary())

    ax.plot(high2, high1, 'r.')

    # Add an axis to the plot
    axi = plt.axis()

    # Initialize `x`
    x = np.linspace(axi[0], axi[1] + 0.01)

    ax.plot(x, results.params[0] + results.params[1] * x, 'b', lw=2)

    ax.set_xlabel(symbols[0])
    ax.set_ylabel(symbols[1])
    ax.legend()

    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tickers_list = ["BTC-USD", "ETH-USD"]
 #   tickers_list = ["TSLA", "CSIQ"]
    testyf(tickers_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
