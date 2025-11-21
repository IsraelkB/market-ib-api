from .bb_break_retest_backtest import run_bb_break_retest_strategy_backtest
from .bb_context import BBContext
from .calc_ratio import run_calc_ratio
from .prepare_stock_bb_data import run_ib_test
from utils_folder.get_data_config import get_config_stock_settings, get_config_bb_settings
from utils_folder.get_path import get_base_path

def bollinger_bands():
    stock_settings = get_config_stock_settings()

    root_path = get_base_path()
    stock_names = stock_settings["stock_names"]

    for stock in stock_names:
        bb_settings = BBContext(stock)
        bb_settings.reset_results()
        csv_name = f"{bb_settings.stock_name}-{stock_settings["bar_size"]}"
        csv_file = f"{root_path}/reports/bars/{bb_settings.stock_name}/{csv_name}.csv"
        try:
            report_path = run_ib_test(stock_settings, csv_file, stock)
            print(f"✅ IB test and data collection finished. Report saved to: {report_path}")
        except Exception as e:
            print(f"❌ Error during IB test: {e}")
            exit()

        print("Starting backtesting strategy...")
        try:
            analyze_path = run_bb_break_retest_strategy_backtest(bb_settings, csv_name, root_path,
                                                                 input_data_path=report_path)
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

    print("\t--- All steps completed successfully! ---")