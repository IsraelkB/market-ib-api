import pandas as pd
from ta.trend import SMAIndicator
import numpy as np

def ma_100(df):
    df['MA_100'] = df['close'].rolling(window=100, min_periods=100).mean()

    print(df[['date', 'close', 'MA_100']].iloc[95:105])

