class Trader:
    def __init__(self, buy_algo, sell_algo):
        self.buyalgo = buy_algo
        self.sellalgo = sell_algo
        self.bought = True


    def update(self, ticker_info):
        if not self.bought:
            self.buy_info = self.buyalgo.update(ticker_info)
            if self.buy_info.do_buy:
                #buy process
                self.bought = True
                return
        sell_info = self.buyalgo.update(ticker_info, self.buy_info)
        if sell_info.do_sell:
            # sell process
            # save result
            self.bought = False
