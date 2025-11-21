from utils_folder.get_files import read_yaml_file


def get_config_bb_settings():
    cfg = read_yaml_file("config_bb.yml")
    return {"sigma_multiplier": cfg["bollinger_sigma"],
            "stop_loss_mode": cfg["stop_loss_mode"],
            "min_bb_break_percent": cfg["min_breakout_percent"],
            "min_delay_after_loss": cfg["loss_cooldown_minutes"],
            "get_in_reverse_candle": cfg["allow_reverse_entry_candle"],
            "policy": cfg["policy"]}

def get_config_stock_settings():
    cfg = read_yaml_file("config_bb.yml")
    print(cfg)
    return {"stock_names": cfg["symbols"],
            "bar_size": cfg["bar_size"],
            "end_data_time": cfg["history_end_time"],
            "duration_time": cfg["history_duration"]}
