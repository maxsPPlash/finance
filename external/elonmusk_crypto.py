import tweepy
from tweepy import OAuthHandler, Stream, StreamListener

from binance.client import Client
from binance.websockets import BinanceSocketManager

import time
import telegram

#name2ticker = {'bitcoin': 'BTCEUR', 'doge': 'DOGEEUR', 'ethereum': 'ETHEUR', 'dogecoin': 'DOGEEUR'}
name2ticker = {'doge': 'DOGEEUR', 'dogecoin': 'DOGEEUR'}
crypto_names = list(name2ticker.keys())

class CryptoListener(StreamListener):
    def __init__(self):
        super(CryptoListener, self).__init__()

        file = open('binance_info.txt') # 1 line key 2 line secret
        bin_cred = file.read().splitlines()

        api_key = bin_cred[0]
        api_secret = bin_cred[1]

        self.client = Client(api_key, api_secret)

        self.traded = False

    def send_message(self, text):
        file = open('telegram_info.txt')  # 1 line key 2 line secret
        tm_cred = file.read().splitlines()
        bot = telegram.Bot(token=tm_cred[0])
        bot.sendMessage(chat_id=int(tm_cred[1]), text=text)

    def token_trade_history(self, msg):
        ''' define how to process incoming WebSocket messages '''
        if msg['e'] != 'error':
            text = 'Bought at {} now at {}'.format(self.coin_price,  msg['a'])
            print(text)

    def inform_trade(self, text, coin):
        message = 'Trading {} because of message "{}"'.format(coin, text)
        print(message)
        self.send_message(message)

    def trade_crypto(self, name):
        ticker = name2ticker[name]

        self.coin_price = float(self.client.get_symbol_ticker(symbol=ticker)['price'])

        eur_trade = 100
        quant = int(eur_trade / self.coin_price)

        order = self.client.create_test_order(
            symbol=ticker,
            side=Client.SIDE_BUY,
            type=Client.ORDER_TYPE_MARKET,
            quantity=quant)

        bsm = BinanceSocketManager(self.client)
        conn_key = bsm.start_symbol_ticker_socket(ticker, self.token_trade_history)
        bsm.start()

        self.traded = True

        print(order)

    def submit_message(self, text):
        if len(text) == 0 or text[0] == '@':
            return

        for coin_nm in crypto_names:
            if coin_nm in text.lower():
                self.inform_trade(text, coin_nm)

                self.trade_crypto(coin_nm)

                return

    def on_status(self, status):
        if self.traded:
            return True

        try:
            if status.user.screen_name == 'elonmusk':
                print('%s (%s at %s)' % (status.text, status.user.screen_name, status.created_at))

                self.submit_message(status.text)

        except BaseException as e:
            print("Error on_status: %s" % str(e))
        return True

    def on_error(self, status):
        print(status)
        return True

def start_stream():
    file = open('twitter_info.txt')
    tw_cred = file.read().splitlines()

    access_token = tw_cred[0]
    access_secret = tw_cred[1]
    consumer_key = tw_cred[2]
    consumer_secret = tw_cred[3]

    # @elonmusk => 44196397
    elon_id = '44196397'

    while True:
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)

            api = tweepy.API(auth)

            twitter_stream = Stream(auth, CryptoListener())
            twitter_stream.filter(follow=[elon_id])
        except BaseException as e:
            print("Error on_status: %s" % str(e))

        time.sleep(1)

def test_message():
    cl = CryptoListener()

    msgs = ['Now Bitcoin is suppa cool!', 'oh my DOGE, ja ja', "@someguy doge bitcoin", "oh its DOGEcoin"]
    cl.submit_message(msgs[3])

if __name__ == '__main__':
#    start_stream()

    test_message()

