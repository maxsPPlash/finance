# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpointpip install pandas_datareader.

def testyf(symbol):
    print(symbol)
    tickerdata = yf.Ticker(symbol)
    tickerinfo = tickerdata.info
#    print(tickerinfo)

    today = datetime.datetime.today().isoformat()

    tickerof = tickerdata.history(interval = '60m', start = '2021-2-2', end = today[:10])
    ph = tickerof['High']
    pl = tickerof['Low']
    print(tickerof.keys())
    pricelast = ph.describe()

#    print(pricelast)

    # Calculate the 20 and 100 days moving averages of the closing prices
#    short_rolling_msft = cl.rolling(window=20).mean()

    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(ph.index, ph, label=symbol+' high')
    ax.plot(pl.index, pl, label=symbol+' low')
#    ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')

    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()

    plt.show()

    print(pricelast)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    testyf('BTC-USD')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
