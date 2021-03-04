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

    tickerof = tickerdata.history(period = '1h', start = '2020-1-1', end = today[:10])
    cl = tickerof['Close']
    pricelast = cl.describe()

#    print(pricelast)

    # Calculate the 20 and 100 days moving averages of the closing prices
    short_rolling_msft = cl.rolling(window=20).mean()
    long_rolling_msft = cl.rolling(window=100).mean()

    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(cl.index, cl, label=symbol)
    ax.plot(short_rolling_msft.index, short_rolling_msft, label='20 days rolling')
    ax.plot(long_rolling_msft.index, long_rolling_msft, label='100 days rolling')

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
