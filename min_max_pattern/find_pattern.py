import os
from ib_insync import *
from pathlib import Path
from config import settings
import pandas as pd
from min_max_pattern.find_extreme_points import find_min, find_max
from min_max_pattern.midify_file import filter_by_time_and_extreme
from utills.time import invert_gtc

bar_size = "2 mins"
duration_time = "1 D" # 600 S - 10 minutes
end_data_time = ""
stock_watch_list = ["rgti"] # test
# stock_watch_list = ["etsy", "smr", "asts", "qubt", "rklb", "upst", "oklo",
#                     "rddt", "alab", "rgti", "rblx", "iren", "mp", "rcat", "qbts",
#                     "clsk", "nne", "vktx", "enph", "crcl", "sndk", "nbis", "crwv", "baba"]

ib = IB()

ib.connect(settings.host, settings.demo_port, clientId=settings.client_id)

current_dir = Path(__file__).parent
parent_dir = current_dir.parent

for stock in stock_watch_list:
    csv_file = f"{parent_dir}/reports/daily_activity/{stock}.csv"
    min_max_file = f"{parent_dir}/reports/min_max/{stock}.csv"
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

    df_combined = df_combined.tail(1000)
    df_combined.to_csv(csv_file, index=False)

    if os.path.exists(min_max_file):
        df_minmax_past = pd.read_csv(min_max_file)
        print(f"Loaded existing min/max data for {stock}: {len(df_minmax_past)} rows")
    else:
        df_minmax_past = pd.DataFrame()
        print(f"No previous min/max file found for {stock}")

    # 10 candles back for max and min value
    i = 0
    min_candle, max_candle =  [], []
    step = 20

    while i < (len(df_combined) - step):
        window = df_combined.iloc[i:i + step]
        min_candle.extend(find_min(window))
        max_candle.extend(find_max(window))
        i += step

    df_min, df_max =  pd.DataFrame(min_candle), pd.DataFrame(max_candle)
    df_min = filter_by_time_and_extreme(df_min, True, ["open","close"])
    df_max = filter_by_time_and_extreme(df_max, False, ["open","close"])
    df_min["type"] = "min"
    df_max["type"] = "max"

    df_minmax_new = pd.concat([df_min, df_max], ignore_index=True)

    if not df_minmax_past.empty:
        df_minmax_combined = pd.concat([df_minmax_past, df_minmax_new])
        df_minmax_combined = df_minmax_combined.drop_duplicates(subset=["date", "type"], keep="last")
    else:
        df_minmax_combined = df_minmax_new

    # sort the combined min max data by start_date
    df_minmax_combined["start_date"] = pd.to_datetime(df_minmax_combined["start_date"], errors="coerce", utc=True)
    df_minmax_combined = df_minmax_combined.sort_values(by="start_date", ascending=True).reset_index(drop=True)

    time_columns = ["start_date", "end_date", "date"]

    invert_gtc(df_minmax_combined, time_columns)

    df_minmax_combined.to_csv(min_max_file, index=False)
    print(f"Updated min/max file for {stock} → {min_max_file} ({len(df_minmax_combined)} total rows)")
