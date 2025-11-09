import os
from ib_insync import *
from pathlib import Path
from config import settings
import pandas as pd
from ib_insync_local.get_stock_data import get_stock_data
from min_max_pattern.double_pattern import find_double_bottom, find_double_top
from min_max_pattern.find_extreme_points import find_min_points, find_max_points
from min_max_pattern.modify_file import filter_by_time_and_extreme
from utills.get_files import open_file_to_read, open_file_to_write
from utills.time import invert_gtc

bar_size = "2 mins"
duration_time = "1 D" # 600 S - 10 minutes
end_data_time = "20251106 23:40:00" # yyyyMMdd HH:mm:ss - 20251105 23:40:00
stock_watch_list = ["smr"] # test
# stock_watch_list = ["etsy", "smr", "asts", "qubt", "rklb", "upst", "oklo",
#                     "rddt", "alab", "rgti", "rblx", "iren", "mp", "rcat", "qbts",
#                     "clsk", "nne", "vktx", "enph", "crcl", "sndk", "nbis", "crwv", "baba"]


for stock in stock_watch_list:
    stock_data_path = f"reports/daily_activity/{stock}"
    min_max_file_path = f"reports/min_max/{stock}"
    past_data = open_file_to_read(stock_data_path)
    df_minmax_past = open_file_to_read(min_max_file_path)


    df_new = get_stock_data(stock, end_data_time, duration_time, bar_size)
    if df_new is None:
        continue

    stock_data = pd.concat([past_data, df_new]).drop_duplicates(subset=["date"], keep="last")

    stock_data = stock_data.tail(1000)
    invert_gtc(stock_data, ["date"])
    open_file_to_write(stock_data_path, stock_data)

    # 10 candles back for max and min value
    i = 0
    min_candle, max_candle =  [], []
    step = 20

    while i < (len(stock_data) - step):
        before = i - 7 if i > 0 else i
        window = stock_data.iloc[before:i + step]
        min_candle.extend(find_min_points(window))
        max_candle.extend(find_max_points(window))
        i += step

    df_min, df_max =  pd.DataFrame(min_candle), pd.DataFrame(max_candle)
    # df_min = filter_by_time_and_extreme(df_min, True, ["open","close"])
    # df_max = filter_by_time_and_extreme(df_max, False, ["open","close"])
    df_min["type"] = "min"
    df_max["type"] = "max"

    df_minmax_new = pd.concat([df_min, df_max], ignore_index=True).drop_duplicates(subset=["date", "type"], keep="last")

    if not df_minmax_past.empty:
        df_minmax_combined = pd.concat([df_minmax_past, df_minmax_new])
        df_minmax_combined = df_minmax_combined.drop_duplicates(subset=["date", "type"], keep="last")
    else:
        df_minmax_combined = df_minmax_new

    # sort the combined min max data by start_date
    df_minmax_combined["date"] = pd.to_datetime(df_minmax_combined["date"], errors="coerce", utc=True)
    df_minmax_combined = df_minmax_combined.sort_values(by="date", ascending=True).reset_index(drop=True)

    invert_gtc(df_minmax_combined, ["start_date", "end_date", "date"])

    df_mins = df_minmax_combined[df_minmax_combined["type"] == "min"].copy()
    df_maxs = df_minmax_combined[df_minmax_combined["type"] == "max"].copy()
    print(find_double_bottom(df_mins))
    print(find_double_top(df_maxs))

    open_file_to_write(min_max_file_path,df_minmax_combined)
    print(f"Updated min/max file for {stock} → {min_max_file_path} ({len(df_minmax_combined)} total rows)")
