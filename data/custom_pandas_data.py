from backtrader.feeds import PandasData

class CustomPandasData(PandasData):
    lines = ('order_book_depth', 'historical_volatility',)

    params = (
        ('datetime_col', 'timestamp'),
        ('order_book_depth', -1),
        ('historical_volatility', -1),
        ('openinterest', None),
    )

    def __init__(self, *args, **kwargs):
        self.datetime_col = kwargs.pop('datetime_col', 'timestamp')
        super().__init__(*args, **kwargs)

    def _load(self):
        if self._idx >= len(self.p.dataname):
            # End of data
            return False

        # Set the standard data
        for col_idx, col_name in enumerate(self.getlinealiases()):
            if col_name == 'openinterest':
                continue
            line = getattr(self.lines, col_name)
            if col_name == 'datetime':
                line[0] = self.date2num(self.p.dataname.iloc[self._idx][self.datetime_col])
            else:
                line[0] = self.p.dataname.iloc[self._idx][col_name]

        # Move to the next bar
        self._idx += 1

        return True
