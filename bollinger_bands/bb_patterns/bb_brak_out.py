from .bb_retest import scan_for_bb_retest_entry
from bollinger_bands.utils import chack_for_cooldown

def handle_brak_out_pattern(list_of_dfs, bb_settings):
    sigma_multiplier = bb_settings.sigma_multiplier
    loss_cooldown_minutes = bb_settings.loss_cooldown_minutes
    for key, value in list_of_dfs.items():
        i = 1
        bb_settings.last_loss_time = None
        while i < len(value):
            row = value[i]

            if chack_for_cooldown(bb_settings.last_loss_time, row, loss_cooldown_minutes) and brak_down_red_candle_policy(value, i, bb_settings):
                i = execute_policy(value, i, row["high"], bb_settings, f"upper_{sigma_multiplier}σ")
            elif chack_for_cooldown(bb_settings.last_loss_time, row, loss_cooldown_minutes) and brak_up_green_candle_policy(value, i, bb_settings):
                i = execute_policy(value, i, row["low"], bb_settings, f"lower_{sigma_multiplier}σ")

            i += 1


def execute_policy(value, curr_row_idx, brak_extreme_point, ctx, upper_bb_key):
    if ctx.policy == "retest":
        return scan_for_bb_retest_entry(ctx, value, curr_row_idx + 1, upper_bb_key)
    return curr_row_idx


def brak_down_red_candle_policy(value, curr_row_idx, ctx):
    lower_bb_key = f"lower_{ctx.sigma_multiplier}σ"
    min_breakout_percent = ctx.min_breakout_percent
    row = value[curr_row_idx]
    percent_ok = abs(row["close"] - row[lower_bb_key]) >= row["close"] * min_breakout_percent
    return row["open"] > row[lower_bb_key] > row["close"] and curr_row_idx + 1 < len(value) and percent_ok


def brak_up_green_candle_policy(value, curr_row_idx, ctx):
    upper_bb_key = f"upper_{ctx.sigma_multiplier}σ"
    min_breakout_percent = ctx.min_breakout_percent
    row = value[curr_row_idx]
    percent_ok = abs(row["close"] - row[upper_bb_key]) >= row["close"] * min_breakout_percent
    return row["open"] < row[upper_bb_key] < row["close"] and curr_row_idx + 1 < len(value) and percent_ok
