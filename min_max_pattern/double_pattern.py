# the same price between 0.5%
# time between 10 minute
# there isn't an extreme point bigger/lower between double top/bottom
from min_max_pattern.min_max_detect import is_cross
import pandas as pd

from utills.time import duration_in_minutes, invert_gtc

percentage_in_pattern = 0.005
percentage_against = 0.005 # if is double top so the second top is above the first one, or in bottom is under the first one.


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
            if duration < 10 or 40 < duration:
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
            if duration < 10 or 40 < duration:
                continue
            if check_for_double_bottom(curr_min, min_val_to_check):
                double_bottom.append([curr_bottom, curr_row])
                break
            elif curr_min < min_val_to_check:
                break

    return double_bottom