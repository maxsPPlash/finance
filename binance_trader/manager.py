import trader

class Manager:
    def register_data_flow(self, source):
        self.data_flow = source

    def init_tickers(self):
        self.tickers = {'AAVEUSDT', 'ADABUSD', 'CHZUSDT'}

    def update(self):
        #dosomething
        pass

    def init_traders(self):
        pass
