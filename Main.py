import os
import sys
from get_statistic.bb_strategy_backtester_for_file import run_backtest
from get_statistic.calc_ratio import run_calc_ratio
from ib_insync_local.ib_insync_test import run_ib_test
from utills.input_utils import collect_bb_settings, collect_stock_settings
from pathlib import Path

sys.path.append(os.path.dirname(__file__))
stock_settings = collect_stock_settings()
bb_settings = collect_bb_settings()

root_path = Path(__file__).parent
csv_name = f"{stock_settings["stock_name"]}_period-{stock_settings["duration_time"]}_bars-{stock_settings["bar_size"]}"
csv_file = f"{root_path}/reports/{csv_name}.csv"
# csv_file = Path(__file__).parent / "reports" / f"{stock_settings["stock_name"]}" / f"{csv_name}.csv"


try:
    report_path = run_ib_test(stock_settings, csv_file)
    print(f"✅ IB test and data collection finished. Report saved to: {report_path}")
except Exception as e:
    print(f"❌ Error during IB test: {e}")
    exit()

print("Starting backtesting strategy...")
try:
    analyze_path = run_backtest(bb_settings, csv_name, {stock_settings["stock_name"]}, root_path, file_path_to_process=report_path)
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