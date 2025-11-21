import os
import pandas as pd


def create_ratio_row_for_file(bb_context, filename, r, success_count, total_trades):
    return {
        "filename": filename,
        "stock_name": bb_context.stock_name,
        "R": r,
        "success_trades": success_count,
        "all_trades": total_trades,
        "ratio": success_count / total_trades,
        "risk_reward_ratio": success_count * r - (total_trades - success_count),
        "sigma_multiplier": bb_context.sigma_multiplier,
        "stop_loss_mode": bb_context.stop_loss_mode,
        "min_breakout_percent": bb_context.min_breakout_percent,
        "loss_cooldown_minutes": bb_context.loss_cooldown_minutes,
        "allow_reverse_candle": bb_context.allow_reverse_candle,
        "policy": bb_context.policy,
    }


def run_calc_ratio(bb_context, root_path, file_path_to_process):
    output_file = f"{root_path}/analyze/success_rate/rate.csv"

    r_ratio_levels = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0,
                      2.1, 2.2, 2.3, 2.4, 2.5]

    ratio_rows = []

    try:
        df = pd.read_csv(file_path_to_process)
        trades = df.to_dict('records')
    except FileNotFoundError:
        print(f"❌ Error: Analysis file not found at {file_path_to_process}")
        return None

    filename = os.path.basename(file_path_to_process)

    total_trades = len(trades)
    if total_trades == 0:
        print(f"⚠ File contains 0 trades, skipping.")
        return None

    for r in r_ratio_levels:
        success_count = sum(1 for row in trades if row["max_profit"] >= r)

        ratio_row = create_ratio_row_for_file(bb_context, filename, r, success_count, total_trades)

        ratio_rows.append(ratio_row)

    # Convert to DataFrame
    new_df = pd.DataFrame(ratio_rows)

    # Merge with existing file
    if os.path.exists(output_file):
        try:
            existing_df = pd.read_csv(output_file)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except Exception as e:
            print(f"❌ Error reading existing success-rate file: {e}")
            combined_df = new_df
    else:
        print(f"💡 Output file does not exist, creating new one: {output_file}")
        combined_df = new_df

    # Save merged results
    combined_df.to_csv(output_file, index=False, encoding='utf-8')

    return output_file
