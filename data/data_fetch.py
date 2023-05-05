import ccxt
import pandas as pd

def fetch_historical_data(exchange, symbol, timeframe='1m', since=None, limit=1000):
    exchange_obj = getattr(ccxt, exchange)()
    candles = exchange_obj.fetch_ohlcv(symbol, timeframe, limit=limit)

    if since:
        since = exchange_obj.parse8601(since)
        candles = exchange_obj.fetch_ohlcv(symbol, timeframe, since=since, limit=limit)
    else:
        candles = exchange_obj.fetch_ohlcv(symbol, timeframe, limit=limit)

    df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df.set_index('timestamp')
