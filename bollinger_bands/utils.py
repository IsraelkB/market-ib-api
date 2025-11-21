from utils_folder.get_data_config import get_config_bb_settings
from utils_folder.time import duration_in_minutes


def unpack_bb_settings():
    bb_settings = get_config_bb_settings()

    sigma_multiplier = bb_settings["sigma_multiplier"]
    stop_loss_mode = bb_settings["stop_loss_mode"]
    min_breakout_percent = bb_settings["min_bb_break_percent"]
    loss_cooldown_minutes = bb_settings["min_delay_after_loss"]
    allow_reverse_candle = bb_settings["get_in_reverse_candle"]
    policy = bb_settings["policy"]

    return sigma_multiplier, stop_loss_mode, min_breakout_percent, loss_cooldown_minutes, allow_reverse_candle, policy


def chack_for_cooldown(last_loss_time, row, loss_cooldown_minutes):
    return last_loss_time is None or duration_in_minutes(last_loss_time,row["date"]) >= loss_cooldown_minutes