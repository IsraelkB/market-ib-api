from allerts.mail_allerts import send_email
import pandas as pd
from min_max_pattern.utils import read_yaml_file
from utils_folder.time import duration_in_minutes, get_list_loc_by_time

cfg = read_yaml_file("config_doubles.yml")
percentage_in_pattern = cfg["percentage_in_pattern"]
percentage_against = cfg["percentage_against"]
until_date = cfg["max_time_for_double"]
candle_duration_minutes = 2

def check_for_double_top(curr_max, max_val_to_check):
    difference = max_val_to_check - curr_max
    if difference < 0 and -difference < percentage_against * curr_max:
        return True
    elif 0 <= difference < percentage_in_pattern * curr_max:
        return True
    return False

def check_for_double_bottom(curr_min, min_val_to_check):
    difference = min_val_to_check - curr_min
    if difference < 0 and -difference < percentage_in_pattern * curr_min:
        return True
    elif 0 <= difference < percentage_against * curr_min:
        return True
    return False


def find_double_top(df):
    double_top = []
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.sort_values(by="date").reset_index(drop=True)
    for i in range (len(df)):
        curr_top = df.iloc[i]
        max_val_to_check = max(curr_top["close"], curr_top["open"])
        for j in range (i, len(df)):
            curr_row = df.iloc[j]
            curr_max = max(curr_row["close"], curr_row["open"])
            duration = duration_in_minutes(curr_top["date"], curr_row["date"])
            if duration < 10 or until_date < duration:
                continue
            if check_for_double_top(curr_max, max_val_to_check):
                double_top.append([curr_top, curr_row])
                break
            elif curr_max > max_val_to_check:
                break
    return double_top


def find_double_bottom(df):
    double_bottom = []
    df["date"] = pd.to_datetime(df["date"], utc=True)
    df = df.sort_values(by="date").reset_index(drop=True)
    for i in range(len(df)):
        curr_bottom = df.iloc[i]
        min_val_to_check = min(curr_bottom["close"], curr_bottom["open"])
        for j in range(i, len(df)):
            curr_row = df.iloc[j]
            curr_min = min(curr_row["close"], curr_row["open"])
            duration = duration_in_minutes(curr_bottom["date"], curr_row["date"])
            if duration < 10 or until_date < duration:
                continue
            if check_for_double_bottom(curr_min, min_val_to_check):
                double_bottom.append([curr_bottom, curr_row])
                break
            elif curr_min < min_val_to_check:
                break

    return double_bottom


def verify_double_top(double_top_list, df_candle):
    global candle_duration_minutes
    new_list = []
    for double in double_top_list:
        latest_max = double[1]
        j = duration_in_minutes(df_candle.iloc[0]["date"], latest_max["date"]) / candle_duration_minutes
        max_of_double = max(latest_max["close"], latest_max["open"])
        # is_double = True
        is_double = is_cross_double_candles(double, df_candle, False)
        j = int(j) + 1
        while j < len(df_candle):
            curr_row = df_candle.iloc[j]
            curr_max = max(curr_row["close"], curr_row["open"])
            if curr_max > max_of_double:
                is_double = False
                break
            j += 1
        if is_double:
            new_list.append(double)
    return new_list


def verify_double_bottom(double_bottom_list, df_candle):
    global candle_duration_minutes
    new_list = []
    for double in double_bottom_list:
        latest_min = double[1]
        j = duration_in_minutes(df_candle.iloc[0]["date"], latest_min["date"]) / candle_duration_minutes
        min_of_double = min(latest_min["close"], latest_min["open"])
        # is_double = True
        is_double = is_cross_double_candles(double, df_candle, True)
        if is_double:
            new_list.append(double)
        j = int(j) + 1
        while j < len(df_candle):
            curr_row = df_candle.iloc[j]
            curr_min = min(curr_row["close"], curr_row["open"])
            if curr_min < min_of_double:
                is_double = False
                break
            j += 1
        if is_double:
            new_list.append(double)
    return new_list



def is_cross_double_candles(curr_double, df_candle, is_bottom):
    global candle_duration_minutes
    def get_min_max_point(first_val, second_val):
        return min(first_val, second_val) if not is_bottom \
            else max(first_val,second_val)

    min_max_first = get_min_max_point(curr_double[0]["open"], curr_double[0]["close"])
    min_max_second = get_min_max_point(curr_double[1]["open"], curr_double[1]["close"])
    min_max_point = get_min_max_point(min_max_first, min_max_second)
    i = duration_in_minutes(df_candle.iloc[0]["date"], curr_double[0]["date"]) / candle_duration_minutes
    until = duration_in_minutes(df_candle.iloc[0]["date"], curr_double[1]["date"]) / candle_duration_minutes
    i = int(i) + 1
    while i < until:
        curr_row = df_candle.iloc[i]
        curr_min_max = get_min_max_point(curr_row["open"], curr_row["close"])
        if is_bottom and curr_min_max > min_max_point:
            return True
        elif not is_bottom and curr_min_max < min_max_point:
            return True
        i += 1
    print(curr_double)
    return False