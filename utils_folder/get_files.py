import glob
import os
from collections import defaultdict
import pandas as pd
from utils_folder.get_path import get_base_path


def get_list_files(path, need_convert_date):
    trade_path = f"C:/Users/Israel/PycharmProjects/market ib api/{path}"

    all_files = glob.glob(os.path.join(trade_path, "*.csv"))
    list_of_dfs = defaultdict(list)

    for filename in all_files:
        try:
            df = pd.read_csv(filename)
            if need_convert_date:
                df['date'] = pd.to_datetime(df['date'])
            list_of_dfs[os.path.basename(filename)] = df.to_dict('records')
        except Exception as e:
            print(f"Error opening file {filename}: {e}")

    return list_of_dfs


def get_local_stock_list(folder):
    files = os.listdir(folder)
    return [f for f in files if not f.startswith(".")]



def open_file_to_read(relative_path):
    root_path = get_base_path()

    csv_file = f"{root_path}/{relative_path}.csv"

    if os.path.exists(csv_file):
        df_combined = pd.read_csv(csv_file)
    else:
        print(f"File {csv_file} does not exist.")
        df_combined = pd.DataFrame()

    return df_combined

def open_file_to_write(relative_path, df):
    root_path = get_base_path()

    csv_file = f"{root_path}/{relative_path}.csv"
    os.makedirs(os.path.dirname(csv_file), exist_ok=True)
    df.to_csv(csv_file, index=False)
