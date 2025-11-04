# 10 minutes min time between double. 40 minutes max time. - DF contain 40 min
# max if the two candles before and the two after him close under.
# min if the two candles before and the two after him close above.
# also if there is the most 4 candle in the same close/open price.
# the percentage distance between the double top/bottom the most is 1%
from min_max_pattern.utils import sequence_ok, chack_boundary, check_deviation_down, check_deviation_up
from utills.time import duration_in_minutes

percentage = 0.01


def is_cross(row, local_min, is_open_min, is_close_min, is_min):
    if not is_open_min:
        if is_min and row["open"] < local_min:
            return True
        elif not is_min and row["open"] > local_min:
            return True
    elif not is_close_min:
        if is_min and  row["close"] < local_min:
            return True
        elif not is_min and  row["close"] > local_min:
            return True
    return False

def is_local_min_max(row, local_min, is_min):
    global percentage
    distance_close = abs(row["close"] - local_min)
    distance_open = abs(row["open"] - local_min)
    is_open_min = (percentage * local_min) >= distance_open >= 0
    is_close_min = (percentage * local_min) >= distance_close >= 0
    if is_cross(row, local_min, is_open_min, is_close_min, is_min):
        return ""
    point_in_candle = "open" if (percentage * local_min) >= distance_open >= 0 \
        else ("close" if (percentage * local_min) >= distance_close >= 0 else "")
    return point_in_candle

def find_seq(local_min_max, i, df, same_price_count, is_min, before_indicate):
    max_same_price = 4
    sequence_count = 0
    j = i
    while same_price_count[0] <= max_same_price:
        # for j, Decision whether I received a minimum without a full pattern followed by a warning
        if sequence_ok(sequence_count, 2):
            return True

        j = chack_boundary(j, len(df), before_indicate)
        if j == -1: # out of bounds
            return True

        row = df.iloc[j]
        is_local = is_local_min_max(row, local_min_max, is_min)
        if is_local != "":
            same_price_count[0] += 1
            continue
        if is_min and check_deviation_down(row, local_min_max):
            return False
        elif not is_min and check_deviation_up(row, local_min_max):
            return False
        else:
            sequence_count += 1
        j += 1
    return False


def chack_two_candle_pattern(i, df, local_min_max, is_min):
    same_price_count = [0]
    find_before = find_seq(local_min_max, i, df, same_price_count, is_min, True)
    find_after = find_seq(local_min_max, i, df, same_price_count, is_min, False)
    return find_before and find_after


def find_double_min(df, is_min):
    time_of_min = [None, None]
    local_min = df.iloc[0]["open"]
    is_double = False
    for i in range(0, len(df)):
        row = df.iloc[i]
        is_local_min = is_local_min_max(row, local_min, is_min)
        if is_local_min != "":
            print(row, local_min, is_local_min, time_of_min)
            is_two_candle_pattern = chack_two_candle_pattern(i, df, local_min, is_min)
            if time_of_min[0] is None and is_two_candle_pattern:
                time_of_min[0] = row["date"]
                is_double = True
                local_min = min(row[is_local_min], local_min)
            elif time_of_min[0] is None:
                continue
            if duration_in_minutes(row["date"], time_of_min[0]) >= 10 and is_two_candle_pattern:
                time_of_min[1] = row["date"]
                is_double = True
                local_min = min(row[is_local_min], local_min)
        elif row["open"] < local_min:
            time_of_min[1] = None
            time_of_min[0] = row["date"]
            is_double = False
            local_min = row["open"]
        elif row["close"] < local_min:
            time_of_min[1] = None
            time_of_min[0] = row["date"]
            is_double = False
            local_min = row["close"]
    return time_of_min


def find_double_max(df, is_min):
    time_of_max = [None, None]
    local_max = df.iloc[0]["open"]
    is_double = False
    for i in range(0, len(df)):
        row = df.iloc[i]
        is_local_max = is_local_min_max(row, local_max, is_min)
        if is_local_max != "":
            print(row, local_max, is_local_max, time_of_max)
            is_two_candle_pattern = chack_two_candle_pattern(i, df, local_max, is_min)
            if time_of_max[0] is None and is_two_candle_pattern:
                time_of_max[0] = row["date"]
                is_double = True
                local_max = max(row[is_local_max], local_max)
            elif time_of_max[0] is None:
                continue
            elif  duration_in_minutes(row["date"], time_of_max[0]) >= 10 and is_two_candle_pattern:
                time_of_max[1] = row["date"]
                is_double = True
                local_max = max(row[is_local_max], local_max)
        elif row["open"] > local_max:
            time_of_max[1] = None
            time_of_max[0] = row["date"]
            is_double = False
            local_max = row["open"]
        elif row["close"] > local_max:
            time_of_max[1] = None
            time_of_max[0] = row["date"]
            is_double = False
            local_max = row["close"]
    return time_of_max

def find_double(df, is_min):
    """
    df: DataFrame of 40 minutes
    is_min: True to search double bottom, False to search double top
    """
    return find_double_min(df, is_min) if is_min else find_double_max(df, is_min)



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
