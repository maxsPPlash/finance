# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import pandas as pd
import yfinance as yf
import datetime
import matplotlib.pyplot as plt
import math

def cur_ms(price, step):
    return math.ceil(price / step) * step

def testyf(symbol, step, days_after):
    print(symbol)
    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 9))

    tickerdata = yf.Ticker(symbol)

    today = datetime.datetime.today().isoformat()

    tickerof = tickerdata.history(interval = '1d', start = '2020-1-1', end = today[:10])
    ph = tickerof['Low']

    ms = cur_ms(ph[0], step)
    i = 0
    l = len(ph)
    while i < l:
        if (ph[i] > ms):
            #pt = ph[i:i+20]
            pt = list()
            next_cnt = min(days_after, l - i)
            for j in range(next_cnt):
                pt.append(ph[i+j] - ph[i])
            ax.plot(list(range(next_cnt)), pt, label=symbol + ' high after ' + str(ms))
            i += days_after
        if(i < l):
            ms = cur_ms(ph[i], step)
        i += 1;

    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()

    plt.show()

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tickers_list = ["BTC-USD", "ETH-USD"]
    testyf(tickers_list[0], 10000, 20)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
