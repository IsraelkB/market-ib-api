import pandas as pd
from ib_insync_local.get_stock_data import get_stock_data
from min_max_pattern.data_rectification import create_df_min, create_df_max, modify_date, connect_dfs
from min_max_pattern.double_pattern import find_double_bottom, find_double_top
from min_max_pattern.find_extreme_points import find_min_points, find_max_points
from utills.get_files import open_file_to_read, open_file_to_write
from utills.time import invert_gtc

bar_size = "2 mins"
duration_time = "1 D" # 600 S - 10 minutes
end_data_time = "20251107 23:40:00" # yyyyMMdd HH:mm:ss - 20251105 23:40:00
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

    # TODO
    #  bugs 1: fix loaded min_max files.
    #  bugs 2: the last candles doesnt checks.
    #  TODO connect to alert.

    while i < (len(stock_data) - step):
        before = i - 7 if i > 0 else i
        window = stock_data.iloc[before:i + step]
        min_candle.extend(find_min_points(window))
        max_candle.extend(find_max_points(window))
        i += step

    df_min, df_max =  create_df_min(min_candle), create_df_max(max_candle)
    df_minmax_new = connect_dfs(df_min, df_max,["date", "type"])

    df_minmax_combined = connect_dfs(df_minmax_past, df_minmax_new,["date", "type"])

    df_minmax_combined = modify_date(df_minmax_combined, ["date", "start_date", "end_date"], ["date", "type"])

    print(find_double_bottom(df_min))
    print(find_double_top(df_max))

    open_file_to_write(min_max_file_path,df_minmax_combined)
    print(f"Updated min/max file for {stock} → {min_max_file_path} ({len(df_minmax_combined)} total rows)")
