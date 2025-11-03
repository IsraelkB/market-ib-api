# 10 minutes min time between double. 40 minutes max time.
# max if the two candles before and after him close under.
# also if there is the most 4 candle in the same close/open price.
# the percentage between double top/bottom the most is 1%

def find_double_min(df):
    local_min = df[0]["open"]
    for row in df:
        if row["open"] > local_min:
            local_min = row["open"]
        elif row["close"] < local_min:
            local_min = row["close"]