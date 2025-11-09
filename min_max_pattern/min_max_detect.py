# the percentage distance between the double top/bottom the most is 1%
from min_max_pattern.utils import sequence_ok, chack_boundary
import pandas as pd

sequence_candle = 2

def is_cross(min_max_val_candle, min_max_to_verify, is_min):
    if min_max_val_candle == min_max_to_verify:
        return "equal"
    if is_min and min_max_val_candle < min_max_to_verify:
        return "cross"
    elif not is_min and min_max_val_candle > min_max_to_verify:
        return "cross"
    return "extreme"

def find_seq(min_max_to_verify, i, df, is_min, before_indicate):
    global sequence_candle
    sequence_count = 0
    j = chack_boundary(i, len(df), before_indicate)
    while j >= 0:
        # for j, Decision whether I received a minimum without a full pattern followed by a warning
        if sequence_ok(sequence_count, sequence_candle):
            return True

        row = df.iloc[j]
        curr_candle_min_max = min(row["open"], row["close"]) if is_min else max(row["open"], row["close"])
        is_cross_extreme = is_cross(curr_candle_min_max, min_max_to_verify, is_min)
        j = chack_boundary(j, len(df), before_indicate)
        if is_cross_extreme == "equal":
            continue
        elif is_cross_extreme == "cross":
            return False
        else:
            sequence_count += 1
    return False


def chack_two_candle_pattern(i, df, local_min_max, is_min):
    find_before = find_seq(local_min_max, i, df, is_min, True)
    find_after = find_seq(local_min_max, i, df, is_min, False)
    return find_before and find_after