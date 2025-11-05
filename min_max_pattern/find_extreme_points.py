# 10 minutes min time between double. 40 minutes max time. - DF contain 40 min
# max if the two candles before and the two after him close under.
# min if the two candles before and the two after him close above.
# also if there is the most 4 candle in the same close/open price.
from min_max_pattern.min_max_detect import chack_two_candle_pattern
from min_max_pattern.utils import init_min_max
import pandas as pd

def find_min(df):
    start_time = df.iloc[0]["date"]
    end_time = df.iloc[-1]["date"]
    min_rows = []
    for i in range(len(df)):
        row = df.iloc[i]
        min_val_candle = min(row["close"], row["open"])
        if chack_two_candle_pattern(i, df, min_val_candle, True):
            min_rows.append(init_min_max(row, start_time, end_time))
    return min_rows



def find_max(df):
    start_time = df.iloc[0]["date"]
    end_time = df.iloc[-1]["date"]
    max_rows = []
    for i in range(0, len(df)):
        row = df.iloc[i]
        max_val_candle = max(row["close"], row["open"])
        if chack_two_candle_pattern(i, df, max_val_candle, False):
            max_rows.append(init_min_max(row, start_time, end_time))
    return max_rows

