from min_max_pattern.data_rectification import connect_dfs, modify_date
from utills.get_files import open_file_to_read, open_file_to_write
import pandas as pd

def sequence_ok(sequence_count, target):
    return sequence_count >= target

def chack_boundary(j, bound, indicate):
    j += -1 if indicate else 1
    return -1 if j < 0 or j >= bound else j

def init_min_max(row, start, end):
    min_row = row.copy()
    min_row["start_date"] = start
    min_row["end_date"] = end
    return min_row

def update_candles_file(stock, df_new):
    stock_data_path = f"reports/daily_activity/{stock}"
    past_data = open_file_to_read(stock_data_path)
    stock_data = connect_dfs(past_data, df_new,["date"])
    stock_data = stock_data.tail(1000)
    stock_data = modify_date(stock_data, ["date"], ["date"])
    open_file_to_write(stock_data_path, stock_data)

def update_min_max_file(stock, df_min, df_max):
    min_max_file_path = f"reports/min_max/{stock}"
    df_minmax_past = open_file_to_read(min_max_file_path)
    df_minmax_new = connect_dfs(df_min, df_max,["date", "type"])
    df_minmax_combined = connect_dfs(df_minmax_past, df_minmax_new,["date", "type"])
    df_minmax_combined = modify_date(df_minmax_combined, ["date", "start_date", "end_date"], ["date", "type"])
    open_file_to_write(min_max_file_path,df_minmax_combined)
    print(f"Updated min/max file for {stock} → {min_max_file_path} ({len(df_minmax_combined)} total rows)")

def update_alert_file(df_double_alert, file_alert):
    df_double_alert = modify_date(df_double_alert, ["date_early", "date_late"], ["date_early", "date_late"])
    open_file_to_write(file_alert,df_double_alert)
