from binance.client import Client
import matplotlib.pyplot as plt
import pandas as pd

def testplot(symbol):
    print(symbol)

    file = open('binance_info.txt')  # 1 line key 2 line secret
    bin_cred = file.read().splitlines()

    api_key = bin_cred[0]
    api_secret = bin_cred[1]

    client = Client(api_key, api_secret)

#    timestamp = client._get_earliest_valid_timestamp(symbol, '1h')
#    print(timestamp)
#    limit = 1000
#    bars = client.get_historical_klines(symbol, '1h', timestamp, limit=limit)
#    bars = bars[:limit]

    bars = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_1HOUR, "30 day ago UTC")

#    print(bars)

    for line in bars:
        del line[5:]

    crypto_df = pd.DataFrame(bars, columns=['date', 'open', 'high', 'low', 'close'])
    crypto_df.set_index('date', inplace=True)
    crypto_df = crypto_df.astype({'high': 'float64', 'low': 'float64'})

    crypto_df['avg'] = crypto_df[['high', 'low']].mean(axis=1)

    high = crypto_df['avg']

    # Calculate the 20 and 100 days moving averages of the closing prices
    avg7 = high.rolling(window=7).mean()
    avg25 = high.rolling(window=25).mean()
    avg99 = high.rolling(window=99).mean()

    # Plot everything by leveraging the very powerful matplotlib package
    fig, ax = plt.subplots(figsize=(16, 3))

    ax.plot(high.index, high, label=symbol)
#    ax.plot(high.index, crypto_df['low'], label='Low')
#    ax.plot(high.index, crypto_df['high'], label='High')
    ax.plot(avg7.index, avg7, label='7 item average')
    ax.plot(avg25.index, avg25, label='25 item average')
    ax.plot(avg99.index, avg99, label='99 item average')

    ax.set_xlabel('Date')
    ax.set_ylabel('Adjusted closing price ($)')
    ax.legend()

    plt.show()

if __name__ == '__main__':
    testplot('AAVEUSDT')