# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt

def testyf(symbols):
    print(symbols)
    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 9))

    for symbol in symbols:
        tickerdata = yf.Ticker(symbol)

        today = datetime.datetime.today().isoformat()

        tickerof = tickerdata.history(interval = '1d', start = '2020-1-1', end = today[:10])
        ph = tickerof['High']
        pl = tickerof['Low']

        ph = ph / ph[0];
        pl = pl / pl[0];

        ax.plot(ph.index, ph, label=symbol + ' high')
        ax.plot(pl.index, pl, label=symbol + ' low')

    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()

    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tickers_list = ["BTC-USD", "ETH-USD"]
    testyf(tickers_list)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
