import collections

class TickerInfo:
    def __init__(self, h, l, v, n):
        self.high = h
        self.low = l
        self.vol = v
        self.num_trades = n


#TickerInfos99 = collections.deque[TickerInfo]


class BuyRes:
    def __init__(self):
        self.do_buy = False


class SellRes:
    def __init__(self):
        self.do_sell = False


class BuyAlgo99cross:
    def __init__(self):
        self.reset()

    def reset(self):
        self.higher_than_99avg = None

    def update(self, history_data):
        res = BuyRes()

        if len(history_data) < 99:
            return res

        cur_price = (history_data[-1].low + history_data[-1].high) / 2.
        avg99_price = 0.
        for v in history_data:
            avg99_price += (v.low + v.high) / 2.

        avg99_price /= 99.

        new_higher_than_99avg = cur_price > avg99_price
        if new_higher_than_99avg and not self.higher_than_99avg:
            res.do_buy = True

        self.higher_than_99avg = new_higher_than_99avg

        return res


class SellAlgoBase:
    def __init__(self):
        self.reset()

    def reset(self):
        self.start_price = None
        self.max_price = 0.

    def update(self, history_data, buy_info: BuyRes):
        cur_price = (history_data[-1].low + history_data[-1].high) / 2.
        res = SellRes()

        if self.start_price is None:
            self.start_price = cur_price

        if abs(cur_price - self.start_price) > self.start_price * 0.01 and cur_price - self.start_price < (self.max_price - self.start_price) * 0.25:
            res.do_sell = True

        self.max_price = max(self.max_price, cur_price)

        return res


class Trader:
    def __init__(self, ticker, buy_algo, sell_algo):
        self.buyalgo = buy_algo
        self.sellalgo = sell_algo
        self.bought = False
        self.buy_info = None
        self.sell_info = None
        self.ticker = ticker

    def update(self, ticker_info):
        if not self.bought:
            self.buy_info = self.buyalgo.update(ticker_info)
            if self.buy_info.do_buy:
                #buy process
                print('Bying [' + self.ticker + '] for ' + str(ticker_info[-1].high))
                self.bought = True
                self.buyalgo.reset()
            return

        sell_info = self.sellalgo.update(ticker_info, self.buy_info)
        if sell_info.do_sell:
            # sell process
            # save result
            print('Selling [' + self.ticker + '] for ' + str(ticker_info[-1].high))
            self.bought = False
            self.sellalgo.reset()
