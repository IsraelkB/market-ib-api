import pandas as pd
from min_max_pattern.modify_file import filter_by_time_and_extreme
from utils_folder.time import invert_gtc

def data_rectification_for_multiple_df(*dfs):
    pass


def create_df_min(min_candle):
    df_min =  pd.DataFrame(min_candle)
    df_min = filter_by_time_and_extreme(df_min, True, ["open","close"])
    df_min["type"] = "min"
    df_min = modify_date(df_min, ["date", "start_date", "end_date"], ["date"])
    return df_min

def create_df_max(max_candle):
    df_max =  pd.DataFrame(max_candle)
    df_max = filter_by_time_and_extreme(df_max, False, ["open","close"])
    df_max["type"] = "max"
    df_max = modify_date(df_max, ["date", "start_date", "end_date"], ["date"])
    return df_max

def modify_date(df, column, drop_duplicates):
    # sort the combined min max data by first date col
    df[column[0]] = pd.to_datetime(df[column[0]], errors="coerce", utc=True)
    df = df.sort_values(by=column[0], ascending=True).reset_index(drop=True)
    invert_gtc(df, column)
    df = df.drop_duplicates(subset=drop_duplicates, keep="last")
    return df

def connect_dfss(df_first, df_last, drop_columns):
    if not df_first.empty and not df_last.empty:
        df_combined = pd.concat([df_first, df_last])
        df_combined = df_combined if not drop_columns else df_combined.drop_duplicates(subset=drop_columns, keep="last")
    elif not df_first.empty:
        df_combined = df_first
    elif not df_last.empty:
        df_combined = df_last
    else:
        print("df_first and df_last are empty")
        df_combined = pd.DataFrame()

    return df_combined
