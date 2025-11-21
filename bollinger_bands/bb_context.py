from bollinger_bands.utils import unpack_bb_settings

class BBContext:
    def __init__(self, stock_name):
        (
            self.sigma_multiplier,
            self.stop_loss_mode,
            self.min_breakout_percent,
            self.loss_cooldown_minutes,
            self.allow_reverse_candle,
            self.policy
        ) = unpack_bb_settings()

        self.stock_name = stock_name.upper()
        self.trade_results_list = []
        self.last_loss_time = None

    def reset_results(self):
        self.trade_results_list.clear()
        self.last_loss_time = None
