import os
import sys
from .bb_strategy_backtester_for_file import run_backtest
from .calc_ratio import run_calc_ratio
from .prepare_stock_bb_data import run_ib_test
from utils_folder.get_data_config import get_config_stock_settings, get_config_bb_settings
from utils_folder.get_path import get_base_path

def bollinger_bands():
    stock_settings = get_config_stock_settings()
    bb_settings = get_config_bb_settings()

    root_path = get_base_path()
    stock_names = stock_settings["stock_names"]

    # csv_file = Path(__file__).parent / "reports" / f"{stock_settings["stock_name"]}" / f"{csv_name}.csv"
    for stock in stock_names:
        csv_name = f"period-{stock_settings["duration_time"]}_bars-{stock_settings["bar_size"]}"
        csv_file = f"{root_path}/reports/bars/{stock}/{csv_name}.csv"
        try:
            report_path = run_ib_test(stock_settings, csv_file, stock)
            print(f"✅ IB test and data collection finished. Report saved to: {report_path}")
        except Exception as e:
            print(f"❌ Error during IB test: {e}")
            exit()

        print("Starting backtesting strategy...")
        try:
            analyze_path = run_backtest(bb_settings, csv_name, stock, root_path,
                                        file_path_to_process=report_path)
            print(f"✅ Backtesting finished. Analysis saved to: {analyze_path}")
        except Exception as e:
            print(f"❌ Error during backtesting: {e}")
            exit()

        print("Starting R-ratio calculation...")
        try:
            ratio_path = run_calc_ratio(bb_settings, root_path, file_path_to_process=analyze_path)
            print(f"✅ Ratio calculation finished. Ratio data saved to: {ratio_path}")
        except Exception as e:
            print(f"❌ Error during ratio calculation: {e}")
            exit()

        print("\n--- All steps completed successfully! ---")