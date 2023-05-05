from backtrader.feeds import PandasData

class CustomPandasData(PandasData):
    params = (('timestamp', 'timestamp'),)
