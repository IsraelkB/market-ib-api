# 10 minutes min time between double. 40 minutes max time. - DF contain 40 min
# max if the two candles before and the two after him close under.
# min if the two candles before and the two after him close above.
# also if there is the most 4 candle in the same close/open price.
# the percentage distance between the double top/bottom the most is 1%

def find_double(df, min):
    """
    df: DataFrame of 40 minutes
    is_min: True to search double bottom, False to search double top
    """
    percentage = 0.01
    max_same_price = 4
    local_min = df[0]["open"]
    is_double = False
    for row in df:
        distance_close = abs(row["close"] - local_min)
        distance_open = abs(row["open"] - local_min)
        if (percentage * local_min) >= distance_close >= 0:
            local_min = min(local_min, row["close"])
            is_double = True
            continue
        elif (percentage * local_min) >= distance_open >= 0:
            local_min = min(local_min, row["open"]) if min else max(local_min, row["open"])
            is_double = True
            continue
        if not min and row["open"] > local_min:
            is_double = False
            local_min = row["open"]
        elif not min and row["close"] > local_min:
            is_double = False
            local_min = row["close"]
        if min and row["open"] < local_min:
            is_double = False
            local_min = row["open"]
        elif min and row["close"] < local_min:
            is_double = False
            local_min = row["close"]

    return is_double



    # # עוברים על כל נר אפשרי במרכז (לבדוק שני נרות לפני ושני נרות אחרי)
    # for i in range(2, len(df) - 2):
    #     center = df.iloc[i]
    #     before = df.iloc[i - 2:i]
    #     after = df.iloc[i + 1:i + 3]
    #
    #     # תנאי: שני נרות לפני ושני נרות אחרי
    #     if is_min:
    #         # נרות לפני/אחרי סוגרים מעל המרכז
    #         if not all(before["close"] > center["close"]) or not all(after["close"] > center["close"]):
    #             continue
    #     else:
    #         # נרות לפני/אחרי סוגרים מתחת למרכז
    #         if not all(before["close"] < center["close"]) or not all(after["close"] < center["close"]):
    #             continue
    #
    #     # בדיקת max 4 נרות עם אותו close/open
    #     same_price_count = sum((df["close"] == center["close"]) | (df["open"] == center["open"]))
    #     if same_price_count > max_same_price:
    #         continue
    #
    #     # בדיקת אחוז מרחק עד 1%
    #     prev_min_max = df.iloc[:i]
    #     for _, row in prev_min_max.iterrows():
    #         distance = abs(row["close"] - center["close"])
    #         if distance / center["close"] > percentage:
    #             break
    #     else:
    #         return True  # אם עבר את כל התנאים
    #
    # return False
