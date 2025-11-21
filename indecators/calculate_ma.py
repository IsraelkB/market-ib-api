import pandas as pd
from ta.trend import SMAIndicator
import numpy as np


def ma_20(df):
    df['MA_100'] = df['close'].rolling(window=20, min_periods=20).mean()


def ma_50(df):
    df['MA_100'] = df['close'].rolling(window=50, min_periods=50).mean()


def ma_100(df):
    df['MA_100'] = df['close'].rolling(window=100, min_periods=100).mean()