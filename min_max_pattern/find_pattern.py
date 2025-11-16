import time
from ib_insync_local.get_stock_data import get_stock_data
from min_max_pattern.data_rectification_methods import create_df_min, create_df_max
from min_max_pattern.find_extreme_points import find_min_points, find_max_points
from min_max_pattern.handle_doubles import detect_for_doubles
from min_max_pattern.utils import update_candles_file, update_min_max_file, read_yaml_file


def min_max():
    cfg = read_yaml_file("config_doubles.yml")
    bar_size = "2 mins"
    duration_time = cfg["candles_to_get"] # 600 S - 10 minutes
    end_data_time = "" # yyyyMMdd HH:mm:ss - 20251105 23:40:00

    while True:
        for stock in cfg["stock_list"]:
            df_new = get_stock_data(stock, end_data_time, duration_time, bar_size)
            if df_new is None:
                print(f"No data received for {stock}")
                continue

            update_candles_file(stock, df_new)

            min_candle, max_candle =  find_min_points(df_new), find_max_points(df_new)
            df_min, df_max =  create_df_min(min_candle), create_df_max(max_candle)

            detect_for_doubles(df_min, df_max, stock)

            update_min_max_file(stock, df_max, df_min)

        # adding functionality for running from user
        print("✅ Completed one full cycle. Sleeping for 10 minutes...")
        time.sleep(cfg["time_to_sleep"]) # השהיה של 10 דקות