import glob
import os
from collections import defaultdict
import pandas as pd

def get_all_files(path, need_convert_date):
    trade_path = f"C:/Users/Israel/PycharmProjects/market ib api/{path}"

    all_files = glob.glob(os.path.join(trade_path, "*.csv"))
    list_of_dfs = defaultdict(list)

    for filename in all_files:
        try:
            df = pd.read_csv(filename)
            if need_convert_date:
                df['date'] = pd.to_datetime(df['date'])
            list_of_dfs[os.path.basename(filename)] = df.to_dict('records')
            print(f"Opened successfully: {filename}")
        except Exception as e:
            print(f"Error opening file {filename}: {e}")

    return list_of_dfs