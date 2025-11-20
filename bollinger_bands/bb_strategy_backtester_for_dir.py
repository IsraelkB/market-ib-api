import csv
import os
from utils_folder.get_files import get_list_files
from utils_folder.input_utils import get_validated_float, get_validated_int
from utils_folder.time import duration_in_minutes

sigma_multiplier = get_validated_int("please insert the mult σ you want\n", 1, 3)
stop_loss_mode = get_validated_int("please insert the number of stp loss policy you want: 0- min/max, 1- candle\n", 0, 1)
min_bb_break_percent = get_validated_float("please insert the min percentage (from the stock price) above/below the bb line\n", 0, 1) * 0.01
min_delay_after_loss = get_validated_int("please insert the time in minutes to delay after unsuccessful trade\n", 0, 60)

sigma_suffix = f"{sigma_multiplier}σ"
trade_results_list = []
last_loss_time = None


def record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, exit_time, exit_fee, max_profit_price, bb_band_trend):
    duration = exit_time - entry_time
    duration_minutes = duration.total_seconds() / 60
    order_type = "SHORT" if stp_loss - entrance_fee > 0 else "LONG"
    trade_risk_units = abs(entrance_fee - stp_loss)
    win_lose_ratio = 1 if trade_risk_units == 0 else abs(exit_fee - entrance_fee) / trade_risk_units
    win_lose_ratio = -win_lose_ratio if stp_loss == exit_fee else win_lose_ratio
    trade_results_list.append({
        "stock_name": stock_name,
        "entry_time": entry_time,
        "Entrance_fee": entrance_fee,
        "stop_loss": stp_loss,
        "exit_time": exit_time,
        "exit_fee": exit_fee,
        "order_type": order_type,
        "win_lose_ratio": win_lose_ratio, # profit/risk
        "σ": sigma_suffix,
        "duration_time": duration_minutes,
        "max_profit": abs(max_profit_price - entrance_fee) / trade_risk_units, # max profit/risk
        "bb_band_trend": bb_band_trend
    })


def execute_trade_simulation(rows, row_number, stp_loss, stock_name, indicate_line, bb_band_trend):
    # get Entrance detail
    entry_time = rows[row_number]["date"]
    entrance_fee = rows[row_number]["close"]
    stp_loss = stp_loss if stop_loss_mode == 0 else \
        (rows[row_number]["high"] if indicate_line.find("upper") != -1 else rows[row_number]["low"])
    max_profit_price = entrance_fee
    trade_risk_units = abs(entrance_fee - stp_loss)

    for row_index in range(row_number + 1, len(rows)):
        curr_row = rows[row_index]
        if indicate_line.find("upper") != -1:
            if curr_row["high"] >= stp_loss:
                active_delay = curr_row["date"]
                record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, curr_row["date"], stp_loss, max_profit_price, bb_band_trend)
                return row_index
            max_profit_price = min(max_profit_price, curr_row["low"])
            if abs(max_profit_price - entrance_fee) >= 2 * trade_risk_units:
                record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, curr_row["date"], max_profit_price, max_profit_price, bb_band_trend)
                return row_index
        else:
            if curr_row["low"] <= stp_loss:
                active_delay = curr_row["date"]
                record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, curr_row["date"], stp_loss, max_profit_price, bb_band_trend)
                return row_index
            max_profit_price = max(max_profit_price, curr_row["high"])
            if abs(max_profit_price - entrance_fee) >= 2 * trade_risk_units:
                record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, curr_row["date"], max_profit_price, max_profit_price, bb_band_trend)
                return row_index
    return None


def scan_for_entry_signal(rows, row_number, stp_loss, stock_name, indicate_line):
    if row_number >= len(rows):
        return None

    last_bb_price = rows[row_number][indicate_line]
    for row_index in range(row_number, len(rows)):
        curr_row = rows[row_index]
        bb_up = curr_row[indicate_line] > last_bb_price
        bb_down = curr_row[indicate_line] < last_bb_price
        bb_band_trend = "UP" if bb_up else ("DOWN" if bb_down else "FLET")

        if indicate_line.find("upper") != -1:
            if curr_row["high"] > stp_loss:
                stp_loss = curr_row["high"]
            if curr_row["close"] < curr_row["open"] and curr_row["close"] < curr_row[indicate_line]:
                return execute_trade_simulation(rows, row_index, stp_loss, stock_name, indicate_line, bb_band_trend)

        else:
            if curr_row["low"] < stp_loss:
                stp_loss = curr_row["low"]
            if curr_row["close"] > curr_row["open"] and curr_row["close"] > curr_row[indicate_line]:
                return execute_trade_simulation(rows, row_index, stp_loss, stock_name, indicate_line, bb_band_trend)

    return None


analyze_csv = f"C:/Users/Israel/PycharmProjects/market ib api/analyze/success_rate_bb_{sigma_suffix}.csv"
list_of_dfs = get_list_files("reports", True)

for key, value in list_of_dfs.items():
    i = 1
    last_loss_time = None
    while i < len(value):
        row = value[i]
        upper_string = f"upper_{sigma_suffix}"
        lower_string = f"lower_{sigma_suffix}"
        if last_loss_time is None or duration_in_minutes(last_loss_time, row["date"]) >= min_delay_after_loss:
            percent_ok = abs(row["close"] - row[lower_string]) >= row["close"] * min_bb_break_percent
            if row["open"] < row[upper_string] < row["close"] and i + 1 < len(value) and percent_ok:
                exit_row = scan_for_entry_signal(value, i + 1, row["high"], key, upper_string)
                i = exit_row + 1 if exit_row is not None else i + 1
            elif row["open"] > row[lower_string] > row["close"] and i + 1 < len(value):
                exit_row = scan_for_entry_signal(value, i + 1, row["low"], key, lower_string)
                i = exit_row + 1 if exit_row is not None else i + 1
            else:
                i += 1

os.makedirs(os.path.dirname(analyze_csv), exist_ok=True)

with open(analyze_csv, mode='w', newline='', encoding='utf-8') as analyze_file:
    headers = ["stock_name", "entry_time", "Entrance_fee", "stop_loss", "exit_time", "exit_fee", "order_type",
               "win_lose_ratio", "σ", "duration_time", "max_profit", "bb_band_trend"]
    writer = csv.writer(analyze_file)
    writer.writerow(headers)

    for row in trade_results_list:
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
            row['bb_band_trend']
        ])

# the entry pattern need to be significant (in percentage maybe 0.1%).
# 10 mins before rth close the bot.
# delay between unsuccessful trades.
# stp loss to the lowest candle you get in.
