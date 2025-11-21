import csv
import os
import pandas as pd
from bollinger_bands.bb_patterns.bb_brak_out import handle_brak_out_pattern


def run_bb_break_retest_strategy_backtest(bb_settings, csv_name, root_path, input_data_path):
    """
    Runs the Bollinger Band backtesting strategy.
    """
    analyze_csv = f"{root_path}/analyze/bb_break_retest_strategy/{csv_name}_backtest_bb_{bb_settings.sigma_multiplier}σ.csv"
    try:
        df = pd.read_csv(input_data_path, parse_dates=['date'])
        list_of_dfs = {bb_settings.stock_name: df.to_dict('records')}
    except FileNotFoundError:
        print(f"❌ Error: Input file not found at {input_data_path}")
        return None

    handle_brak_out_pattern(list_of_dfs, bb_settings)

    os.makedirs(os.path.dirname(analyze_csv), exist_ok=True)

    with open(analyze_csv, mode='w', newline='', encoding='utf-8') as analyze_file:
        # ... (Keep the CSV writing logic)
        headers = ["stock_name", "entry_time", "Entrance_fee", "stop_loss", "exit_time", "exit_fee", "order_type",
                   "risk_reward_ratio", "σ", "duration_time", "max_profit", "bb_trend"]
        writer = csv.writer(analyze_file)
        writer.writerow(headers)

        for row in bb_settings.trade_results_list:
            writer.writerow([
                row['stock_name'],
                row['entry_time'],
                row['Entrance_fee'],
                row['stop_loss'],
                row['exit_time'],
                row['exit_fee'],
                row['order_type'],
                row['risk_reward_ratio'],
                row['σ'],
                row['duration_time'],
                row["max_profit"],
                row['bb_trend']
            ])

    return analyze_csv  # Return the path to the created analyze CSV



