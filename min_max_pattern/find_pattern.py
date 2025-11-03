import os
from ib_insync import *
from pathlib import Path
from config import settings
import pandas as pd
from min_max_pattern.find_double import find_double

bar_size = "2 min"
duration_time = "600 S" # 10 minutes
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

    df = util.df(bars)
    past_data = pd.read_csv(csv_file)
    file_data = {os.path.basename(csv_file): df.to_dict('records')}
    df.update(file_data)

    is_double_bottom = find_double(df[-40:], True)
    is_double_top = find_double(df[-40:], False)

    if is_double_bottom and is_double_top:
        continue

    elif is_double_bottom:
        print(f"{stock} is double bottom")

    elif is_double_top:
        print(f"{stock} is double top")

    else:
        continue


