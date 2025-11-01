import csv
import glob
import os
import pandas as pd
from collections import defaultdict


sigma_calculated = "1σ"
analyze_df = []


def close_position(entry_time, Entrance_fee, stp_loss, key, exit_time, exit_fee, max_profit_price, bb_trend):
    duration = exit_time - entry_time
    duration_minutes = duration.total_seconds() / 60
    order_type = "SHORT" if stp_loss - Entrance_fee > 0 else "LONG"
    risk_amount = abs(Entrance_fee - stp_loss)
    win_lose_ratio = abs(exit_fee - Entrance_fee) / risk_amount
    win_lose_ratio = -win_lose_ratio if stp_loss == exit_fee else win_lose_ratio
    analyze_df.append({
        "stock_name": key,
        "entry_time": entry_time,
        "Entrance_fee": Entrance_fee,
        "stop_loss": stp_loss,
        "exit_time": exit_time,
        "exit_fee": exit_fee,
        "order_type": order_type,
        "win_lose_ratio": win_lose_ratio, # profit/risk
        "σ": sigma_calculated,
        "duration_time": duration_minutes,
        "max_profit": abs(max_profit_price - Entrance_fee) / risk_amount, # max profit/risk
        "bb_trend": bb_trend
    })


def get_performance_data(value, row_number, stp_loss, key, indicate_line, bb_trend):
    # get Entrance detail
    entry_time = value[row_number]["date"]
    Entrance_fee = value[row_number][indicate_line]
    max_profit_price = Entrance_fee
    risk_amount = abs(Entrance_fee - stp_loss)
    for i in range(row_number + 1, len(value)):
        curr_row = value[i]
        if indicate_line.find("upper") != -1:
            if curr_row["high"] >= stp_loss:
                close_position(entry_time, Entrance_fee, stp_loss, key, curr_row["date"], stp_loss, max_profit_price, bb_trend)
                return i
            max_profit_price = min(max_profit_price, curr_row["low"])
            if abs(max_profit_price - Entrance_fee) >= 2 * risk_amount:
                close_position(entry_time, Entrance_fee, stp_loss, key, curr_row["date"], max_profit_price, max_profit_price, bb_trend)
                return i
        else:
            if curr_row["low"] <= stp_loss:
                close_position(entry_time, Entrance_fee, stp_loss, key, curr_row["date"], stp_loss, max_profit_price, bb_trend)
                return i
            max_profit_price = max(max_profit_price, curr_row["high"])
            if abs(max_profit_price - Entrance_fee) >= 2 * risk_amount:
                close_position(entry_time, Entrance_fee, stp_loss, key, curr_row["date"], max_profit_price, max_profit_price, bb_trend)
                return i
    return None


def find_back_point(value, row_number, stp_loss, key, indicate_line):
    bb_up = True
    bb_down = True
    bb_trend = ""
    last_bb_price = value[row_number][indicate_line]
    for i in range(row_number, len(value)):
        curr_row = value[i]
        bb_up = curr_row[indicate_line] > last_bb_price
        bb_up = curr_row[indicate_line] < last_bb_price
        bb_trend = "UP" if bb_up else ("DOWN" if bb_down else "FLET")

        if indicate_line.find("upper") != -1:
            if curr_row["close"] < curr_row["open"] and curr_row["low"] < curr_row[indicate_line]:
                return get_performance_data(value, i, stp_loss, key, indicate_line, bb_trend)
            if curr_row["high"] > stp_loss:
                stp_loss = curr_row["high"]

        else:
            if curr_row["close"] > curr_row["open"] and curr_row["high"] > curr_row[indicate_line]:
                return get_performance_data(value, i, stp_loss, key, indicate_line, bb_trend)
            if curr_row["low"] < stp_loss:
                stp_loss = curr_row["low"]
    return None


analyze_csv = f"C:/Users/Israel/PycharmProjects/market ib api/analyze/success_rate_bb.csv"
report_path = f"C:/Users/Israel/PycharmProjects/market ib api/reports"

all_files = glob.glob(os.path.join(report_path, "*.csv"))
list_of_dfs = defaultdict(list)

for filename in all_files:
    try:
        df = pd.read_csv(filename)
        df['date'] = pd.to_datetime(df['date'])
        list_of_dfs[os.path.basename(filename)] = df.to_dict('records')
        print(f"Opened successfully: {filename}")
    except Exception as e:
        print(f"Error opening file {filename}: {e}")

# if list_of_dfs:
#     combined_df = pd.concat(list_of_dfs, ignore_index=True)

for key, value in list_of_dfs.items():
    for i in range(1, len(value)):
        row = value[i]
        upper_string = f"upper_{sigma_calculated}"
        lower_string = f"lower_{sigma_calculated}"
        if row["open"] < row[upper_string] < row["close"]:
            exit_row = find_back_point(value, i + 1, row["high"], key, upper_string)
            i = exit_row if exit_row is not None else i
        elif row["open"] > row[lower_string] > row["close"]:
            exit_row = find_back_point(value, i + 1, row["low"], key, lower_string)
            i = exit_row if exit_row is not None else i

os.makedirs(os.path.dirname(analyze_csv), exist_ok=True)

with open(analyze_csv, mode='w', newline='', encoding='utf-8') as analyze_file:
    headers = ["stock_name", "entry_time", "Entrance_fee", "stop_loss", "exit_time", "exit_fee", "order_type",
               "win_lose_ratio", "σ", "duration_time", "max_profit", "bb_trend"]
    writer = csv.writer(analyze_file)
    writer.writerow(headers)

    for row in analyze_df:
        writer.writerow([
            row['stock_name'],
            row['entry_time'],
            row['Entrance_fee'],
            row['stop_loss'],
            row['exit_time'],
            row['exit_fee'],
            row['order_type'],
            row['win_lose_ratio'],
            row['σ'],
            row['duration_time'],
            row["max_profit"],
            row['bb_trend']
        ])