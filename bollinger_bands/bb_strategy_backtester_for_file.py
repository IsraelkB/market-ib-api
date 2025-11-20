import csv
import os
import pandas as pd
from utils_folder.time import duration_in_minutes

# Define global lists/variables or make them part of the function scope if they need to be reset
trade_results_list = []
last_loss_time = None
sigma_multiplier = None
stop_loss_mode = None
min_bb_break_percent = None
min_delay_after_loss = None
sigma_suffix = None

def record_trade_result(entry_time, entrance_fee, stp_loss, stock_name, exit_time, exit_fee, max_profit_price, bb_band_trend):
    global trade_results_list, sigma_suffix
    duration_minutes = duration_in_minutes(exit_time, entry_time)
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
    global stop_loss_mode, last_loss_time
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


def run_backtest(bb_settings,csv_name, stock_name, root_path, file_path_to_process):
    """
    Runs the Bollinger Band backtesting strategy.
    """
    global sigma_multiplier, stop_loss_mode, min_bb_break_percent, min_delay_after_loss, sigma_suffix, trade_results_list, last_loss_time

    # Unpack settings
    (sigma_multiplier, stop_loss_mode, min_bb_break_percent,
     min_delay_after_loss, get_in_reverse_candle) = (bb_settings["sigma_multiplier"], bb_settings["stop_loss_mode"],
                                                     bb_settings["min_bb_break_percent"], bb_settings["min_delay_after_loss"],
                                                     bb_settings["get_in_reverse_candle"])

    # Convert min_bb_break_percent to the required format
    min_bb_break_percent *= 0.01

    sigma_suffix = f"{sigma_multiplier}σ"
    trade_results_list = []  # Reset for a clean run
    last_loss_time = None

    # ... (Rest of the original script's logic starts here)

    analyze_csv = f"{root_path}/analyze/{csv_name}_backtest_bb_{sigma_suffix}.csv"
    try:
        df = pd.read_csv(file_path_to_process, parse_dates=['date'])
        stock_name = os.path.basename(file_path_to_process).split('_bars')[0]
        list_of_dfs = {stock_name: df.to_dict('records')}
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {file_path_to_process}")
        return None

    for key, value in list_of_dfs.items():
        i = 1
        last_loss_time = None
        while i < len(value):
            row = value[i]
            upper_string = f"upper_{sigma_suffix}"
            lower_string = f"lower_{sigma_suffix}"
            if last_loss_time is None or duration_in_minutes(last_loss_time,
                                                             row["date"]) >= min_delay_after_loss:
                percent_ok = abs(row["close"] - row[lower_string]) >= row["close"] * min_bb_break_percent
                if row["open"] < row[upper_string] < row["close"] and i + 1 < len(value) and percent_ok:
                    exit_row = scan_for_entry_signal(value, i + 1, row["high"], stock_name, upper_string)
                    i = exit_row + 1 if exit_row is not None else i + 1
                elif row["open"] > row[lower_string] > row["close"] and i + 1 < len(value):
                    exit_row = scan_for_entry_signal(value, i + 1, row["low"], stock_name, lower_string)
                    i = exit_row + 1 if exit_row is not None else i + 1
                else:
                    i += 1

    os.makedirs(os.path.dirname(analyze_csv), exist_ok=True)

    with open(analyze_csv, mode='w', newline='', encoding='utf-8') as analyze_file:
        # ... (Keep the CSV writing logic)
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

    return analyze_csv  # Return the path to the created analyze CSV



