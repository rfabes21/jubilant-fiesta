import backtrader as bt
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class CryptoArbitrage(bt.Strategy):
    params = (
        ("trade_fee", 0.0025),
        ("threshold_multiplier", 3.5),
        ("atr_period", 14),
        ("risk_percentage", 0.01),  # Use 1% of available cash for each trade
    )

    def __init__(self):
        self.target_token = self.datas
        self.atr = {data: bt.indicators.ATR(data, period=self.params.atr_period) for data in self.target_token}
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
            logging.info(f'Trade: PnL: {trade.pnl:.2f}, Total Profit: {self.total_profit:.2f}, Win Rate: {win_rate:.2f}%')

    def next(self):
        for i, data1 in enumerate(self.target_token):
            for j, data2 in enumerate(self.target_token):
                if i != j:
                    buy_price = data1.close[0]
                    sell_price = data2.close[0]

                    TTS = sell_price - buy_price
                    TAPV = (data1.close[0] * self.params.trade_fee) + (data2.close[0] * self.params.trade_fee)
                    threshold = self.params.threshold_multiplier * max(self.atr[data1][0], self.atr[data2][0])

                    if TTS >= TAPV + threshold:
                        cash = self.broker.getcash()
                        trade_cash = cash * self.params.risk_percentage
                        size = trade_cash / data1.close[0]

                        buy_limit_price = buy_price * (1 + self.params.trade_fee)
                        sell_limit_price = sell_price * (1 - self.params.trade_fee)

                        self.buy(data=data1, size=size, exectype=bt.Order.Limit, price=buy_limit_price)
                        self.sell(data=data2, size=size, exectype=bt.Order.Limit, price=sell_limit_price)
                        logging.info(f"Buy signal on {data1._name}: {data1.datetime.datetime()}, Cash: {self.broker.getcash()}, Value: {self.broker.getvalue()}")
                        logging.info(f"Sell signal on {data2._name}: {data2.datetime.datetime()}, Cash: {self.broker.getcash()}, Value: {self.broker.getvalue()}")