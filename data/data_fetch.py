import ccxt
import pandas as pd
import numpy as np


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

    # Fetch order book depth
    order_book = exchange_obj.fetch_order_book(symbol)
    df['bid'] = order_book['bids'][0][0] if len(order_book['bids']) > 0 else None
    df['ask'] = order_book['asks'][0][0] if len(order_book['asks']) > 0 else None

    # Calculate order book depth (spread)
    df['order_book_depth'] = df['ask'] - df['bid']

    # Calculate historical volatility
    df['log_returns'] = (df['close'] / df['close'].shift(1)).apply(lambda x: np.log(x))
    df['historical_volatility'] = df['log_returns'].rolling(window=21).std() * np.sqrt(252)

    return df.set_index('timestamp')
