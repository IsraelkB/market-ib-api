from AWS.S3.s3_files_menegment import update_file_s3, open_file_to_read_s3
from min_max_pattern.data_rectification_methods import connect_dfss, modify_date
# from utils_folder.get_files import open_file_to_read, open_file_to_write
from typing import Any
import yaml

from utils_folder.get_path import get_path


def read_yaml_file(file_path: str) -> Any:
    root_path = get_path()
    file_path = root_path / file_path
    if not file_path.exists():
        raise FileNotFoundError(f"YAML file not found: {file_path}")

    with file_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data

if __name__ == "__main__":
    try:
        cfg = read_yaml_file("min_max_pattern/config.yml")
        print("Loaded YAML:", cfg)
    except FileNotFoundError as e:
        print("Error:", e)
    except yaml.YAMLError as e:
        print("YAML parse error:", e)


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
    past_data = open_file_to_read_s3(stock_data_path)
    # past_data = open_file_to_read(stock_data_path) # local
    stock_data = connect_dfss(past_data, df_new, ["date"])
    stock_data = stock_data.tail(1000)
    stock_data = modify_date(stock_data, ["date"], ["date"])
    update_file_s3(stock_data, stock_data_path)
    # open_file_to_write(stock_data_path, stock_data) # local

def update_min_max_file(stock, df_min, df_max):
    min_max_file_path = f"reports/min_max/{stock}"
    df_minmax_past = open_file_to_read_s3(min_max_file_path)
    # df_minmax_past = open_file_to_read(min_max_file_path) # local
    df_minmax_new = connect_dfss(df_min, df_max, ["date", "type"])
    df_minmax_combined = connect_dfss(df_minmax_past, df_minmax_new, ["date", "type"])
    df_minmax_combined = modify_date(df_minmax_combined, ["date", "start_date", "end_date"], ["date", "type"])
    update_file_s3(df_minmax_combined, min_max_file_path)
    # open_file_to_write(min_max_file_path,df_minmax_combined) # local
    print(f"Updated min/max file for {stock} → {min_max_file_path} ({len(df_minmax_combined)} total rows)")

def update_alert_file(df_double_alert, file_alert):
    if df_double_alert.empty:
        return
    df_double_alert = modify_date(df_double_alert, ["date_early", "date_late"], ["date_early", "date_late"])
    update_file_s3(df_double_alert, file_alert)
    # open_file_to_write(file_alert,df_double_alert) # local
