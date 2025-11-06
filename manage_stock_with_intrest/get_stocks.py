import pandas as pd
from utills.get_files import open_file_to_read, open_file_to_write

relative_path = "manage_stock_with_intrest/data"
csv_files = ["deals.csv", "stock_list.csv"]

deals = {}
pattern = {}

def get_amount(dict_data, df_data):
    for _, row in df_data.iterrows():
        curr_stock = row["Fin Inst"]
        dict_data[curr_stock] = dict_data.get(curr_stock, 0) + 1


df = open_file_to_read(f"{relative_path}/deals")
get_amount(deals, df)
df = open_file_to_read(f"{relative_path}/stock_list")
get_amount(pattern, df)

pattern_df = pd.DataFrame(list(pattern.items()), columns=["stock_name", "Count"])
deals_df = pd.DataFrame(list(deals.items()), columns=["stock_name", "Count"])
open_file_to_write(f"{relative_path}/pattern_sum", pattern_df)
open_file_to_write(f"{relative_path}/deals_sum", deals_df)
