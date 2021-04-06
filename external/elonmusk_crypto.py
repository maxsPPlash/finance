import tweepy
from tweepy import OAuthHandler, Stream, StreamListener
import yfinance as yf
from datetime import date,timedelta
import matplotlib.pyplot as plt
import time
import numpy

#crypto_names = ['bitcoin cash', 'bitcoin', 'doge', 'ethereum', 'litecoin', 'cardano']
#name2ticker = {crypto_names[0]: '', 2: 'For', 3: 'Geeks'}

#crypto_names = ['bitcoin', 'doge', 'ethereum']
name2ticker = {'bitcoin': 'BTC-USD', 'doge': 'DOGE-USD', 'ethereum': 'ETH-USD', 'dogecoin': 'DOGE-USD'}
crypto_names = list(name2ticker.keys())

def cur_price(ticker):
    tickerdata = yf.Ticker(ticker)

    today = date.today()
    tomorrow = date.today() + timedelta(days=1)

    tickerof = tickerdata.history(interval='1m', start=today.isoformat()[:10], end=tomorrow.isoformat()[:10])
    high = tickerof['High']

    return high[-1];

def inform_trade(text, coin):
    print('Trading {} because of message {}'.format(coin, text))

def trade_crypto(name):
    ticker = name2ticker[name]
    start = cur_price(ticker)

    change = []
    change_id = []

#    plt.ion()
    plt.show()
    plt.pause(0.1)

    fig, ax = plt.subplots(figsize=(16, 9))

    ax.plot(change_id, change, label=name)

    ax.set_xlabel('Minute')
    ax.set_ylabel('Price diff')
    ax.legend()

    i = 0
    while True:
        change_id.append(i)
        i += 1
        change.append(cur_price(ticker) - start)

        #cur_plot.set_xdata(numpy.append(cur_plot.get_xdata(), i))
        #cur_plot.set_ydata(numpy.append(cur_plot.get_ydata(), i))

        ax.clear()
        ax.plot(change_id, change, label=name)

        fig.canvas.draw()
        plt.pause(60)


def submit_message(text):
    for coin_nm in crypto_names:
        if coin_nm in text.lower():
            inform_trade(text, coin_nm)

            trade_crypto(coin_nm)


class CryptoListener(StreamListener):
    def on_status(self, status):
        try:
            if status.user.screen_name == 'elonmusk':
                print('%s (%s at %s)' % (status.text, status.user.screen_name, status.created_at))

                submit_message(status.text)

        except BaseException as e:
            print("Error on_status: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def start_stream():
    access_token = '1378102406693675009-akhaJ9gdAa0VdVZXUtuhMCNRPOtVFU'
    access_secret = 'JvpykChNr7jr6IVeIog5hPlSSfHKgUtG7AQGACbFYN9IM'
    consumer_key = 'qiXSMzir0JE0zXOQIdQoasumX'
    consumer_secret = 'K9721VTgDZJWWn6rqQwAmGYSfUVv60ZJwmlYgA6HPwcL1tPnq0'

    # @elonmusk => 44196397
    elon_id = '44196397'

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    api = tweepy.API(auth)

    twitter_stream = Stream(auth, CryptoListener())
    twitter_stream.filter(follow=[elon_id])

def test_message():
    msgs = ['Now Bitcoin is suppa cool!', 'oh my DOGE ja ja']
    submit_message(msgs[1])

if __name__ == '__main__':
    start_stream()
#    test_message()

