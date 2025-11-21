from utils_folder.time import duration_in_minutes


def record_trade_result(ctx, entry_time, entrance_fee, stop_loss, exit_time, exit_fee, max_profit_price, bb_trend):
    duration_minutes = duration_in_minutes(exit_time, entry_time)

    order_type = "SHORT" if stop_loss - entrance_fee > 0 else "LONG"
    trade_risk_units = abs(entrance_fee - stop_loss)
    risk_reward_ratio = 1 if trade_risk_units == 0 else abs(exit_fee - entrance_fee) / trade_risk_units
    risk_reward_ratio = -risk_reward_ratio if stop_loss == exit_fee else risk_reward_ratio

    ctx.trade_results_list.append({
        "stock_name": ctx.stock_name,
        "entry_time": entry_time,
        "Entrance_fee": entrance_fee,
        "stop_loss": stop_loss,
        "exit_time": exit_time,
        "exit_fee": exit_fee,
        "order_type": order_type,
        "risk_reward_ratio": risk_reward_ratio, # profit/risk
        "σ": f"{ctx.sigma_multiplier}σ",
        "duration_time": duration_minutes,
        "max_profit": abs(max_profit_price - entrance_fee) / trade_risk_units, # max profit/risk
        "bb_trend": bb_trend
    })


def execute_trade_simulation(ctx, rows, row_number, stop_loss, indicate_line, bb_trend):
    entry_time = rows[row_number]["date"]
    entry_price = rows[row_number]["close"]
    stop_loss = stop_loss if ctx.stop_loss_mode == 0 else \
        (rows[row_number]["high"] if indicate_line.find("upper") != -1 else rows[row_number]["low"])
    max_profit_price = entry_price
    trade_risk_units = abs(entry_price - stop_loss)
    for row_index in range(row_number + 1, len(rows)):
        curr_row = rows[row_index]
        if indicate_line.find("upper") != -1:
            if curr_row["high"] >= stop_loss:
                record_trade_result(ctx, entry_time, entry_price, stop_loss, curr_row["date"], stop_loss, max_profit_price, bb_trend)
                return row_index
            max_profit_price = min(max_profit_price, curr_row["low"])
            if abs(max_profit_price - entry_price) >= 2 * trade_risk_units:
                record_trade_result(ctx, entry_time, entry_price, stop_loss, curr_row["date"], max_profit_price, max_profit_price, bb_trend)
                return row_index
        else:
            if curr_row["low"] <= stop_loss:
                record_trade_result(ctx, entry_time, entry_price, stop_loss, curr_row["date"], stop_loss, max_profit_price, bb_trend)
                return row_index
            max_profit_price = max(max_profit_price, curr_row["high"])
            if abs(max_profit_price - entry_price) >= 2 * trade_risk_units:
                record_trade_result(ctx, entry_time, entry_price, stop_loss, curr_row["date"], max_profit_price, max_profit_price, bb_trend)
                return row_index
    return len(rows) - 1


def scan_for_bb_retest_entry(ctx, rows, row_number, bb_band_key):
    if row_number >= len(rows):
        return None

    stop_loss = rows[row_number]["high"] if bb_band_key.find("upper") != -1 else rows[row_number]["low"]
    last_bb_price = rows[row_number][bb_band_key]
    row_index = row_number
    for row_index in range(row_number, len(rows)):
        curr_row = rows[row_index]
        bb_up = curr_row[bb_band_key] > last_bb_price
        bb_down = curr_row[bb_band_key] < last_bb_price
        bb_trend = "UP" if bb_up else ("DOWN" if bb_down else "FLET")

        if bb_band_key.find("upper") != -1:
            if curr_row["high"] > stop_loss:
                stop_loss = curr_row["high"]
            if curr_row["close"] < curr_row["open"] and curr_row["close"] < curr_row[bb_band_key]:
                return execute_trade_simulation(ctx, rows, row_index, stop_loss, bb_band_key, bb_trend)

        else:
            if curr_row["low"] < stop_loss:
                stop_loss = curr_row["low"]
            if curr_row["close"] > curr_row["open"] and curr_row["close"] > curr_row[bb_band_key]:
                return execute_trade_simulation(ctx, rows, row_index, stop_loss, bb_band_key, bb_trend)

    return row_index