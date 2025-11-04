import os
from ib_insync import *
from pathlib import Path
from config import settings
import pandas as pd
from min_max_pattern.find_double import find_double


bar_size = "2 mins"
duration_time = "2 D" # 600 S - 10 minutes
end_data_time = ""
stock_watch_list = ["etsy", "smr", "asts", "qubt", "rklb", "upst", "oklo",
                    "rddt", "alab", "rgti", "rblx", "iren", "mp", "rcat", "qbts",
                    "clsk", "nne", "vktx", "enph", "crcl", "sndk", "nbis", "crwv", "baba"]

ib = IB()

ib.connect(settings.host, settings.demo_port, clientId=settings.client_id)

current_dir = Path(__file__).parent
parent_dir = current_dir.parent

for stock in stock_watch_list:
    csv_file = f"{parent_dir}/reports/daily_activity/{stock}.csv"
    curr_stock = Stock(stock, "SMART", "USD")

    if stock is None:
        print("Stock name not found")
        continue

    bars = ib.reqHistoricalData(
        curr_stock,
        endDateTime=end_data_time,
        durationStr=duration_time,
        barSizeSetting=bar_size,
        whatToShow='MIDPOINT',
        useRTH=True,
    )

    df_new = util.df(bars)

    if os.path.exists(csv_file):
        past_data = pd.read_csv(csv_file)
        df_combined = pd.concat([past_data, df_new]).drop_duplicates(subset=["date"], keep="last")
    else:
        df_combined = df_new

    is_double_bottom = find_double(df_combined[-40:], True)
    is_double_top = find_double(df_combined[-40:], False)

    if is_double_bottom[1] is not None:
        print(f"{stock} has double bottom, in the time range: {is_double_bottom}")

    if is_double_top[1] is not None:
        print(f"{stock} has double top, in the time range: {is_double_top}")


    df_combined = df_combined.tail(1000)
    df_combined.to_csv(csv_file, index=False)
