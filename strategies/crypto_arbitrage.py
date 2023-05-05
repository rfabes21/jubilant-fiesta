import backtrader as bt
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CryptoArbitrage(bt.Strategy):
    params = (
        ('threshold', 0.01),
        ('trade_fee', 0.001),
    )


    def __init__(self):
        self.target_token = [data for data in self.datas]
        self.trades = 0
        self.wins = 0
        self.total_profit = 0

    def log(self, txt, dt=None):
        dt = dt or self.data.datetime.datetime(0)
        print(f'{dt.isoformat()} {txt}')

    def notify_trade(self, trade):
        if trade.isclosed:
            self.trades += 1
            self.total_profit += trade.pnl
            if trade.pnl > 0:
                self.wins += 1
            win_rate = self.wins / self.trades * 100
            self.log(f'Trade: PnL: {trade.pnl:.2f}, Total Profit: {self.total_profit:.2f}, Win Rate: {win_rate:.2f}%')

    def next(self):
        for i, data1 in enumerate(self.target_token):
            for j, data2 in enumerate(self.target_token):
                if i != j:
                    buy_price = data1.close[0]
                    sell_price = data2.close[0]

                    TTS = sell_price - buy_price
                    TAPV = (data1.close[0] * self.params.trade_fee) + (data2.close[0] * self.params.trade_fee)

                    if TTS >= TAPV + self.params.threshold:
                        size = self.broker.getcash() / data1.close[0]
                        self.buy(data=data1, size=size)
                        self.sell(data=data2, size=size)
                        logging.info(f"Buy signal on {data1._name}: {data1.datetime.datetime()}, Cash: {self.broker.getcash()}, Value: {self.broker.getvalue()}")
                        logging.info(f"Sell signal on {data2._name}: {data2.datetime.datetime()}, Cash: {self.broker.getcash()}, Value: {self.broker.getvalue()}")