import os
import pandas as pd

def run_calc_ratio(settings, root_path, file_path_to_process):
    # note = collect_user_settings("stop loss", "percentage for entry", "time to delay after unsuccessful trade", "mult σ, ")
    ratio_file_dir = f"{root_path}/analyze/success_rate/rate.csv"
    R_ratio = [1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5]
    ratio_csv_data = []
    bb_settings = {}
    try:
        df = pd.read_csv(file_path_to_process)
        file_data = {os.path.basename(file_path_to_process): df.to_dict('records')}
        print(df, file_data)
    except FileNotFoundError:
        print(f"❌ Error: Analysis file not found at {file_path_to_process}")
        return None

    for filename, value in file_data.items():
        for r in R_ratio:
            success_count = 0
            all_rows = len(value)
            if all_rows == 0:
                continue
            for row in value:
                if row["max_profit"] >= r:
                    success_count += 1
            new_data = {"filename": filename, "R": r, "success_trades": success_count, "all_trades": all_rows,
                        "ratio": success_count / all_rows, "win/lose_ratio": success_count * r - (all_rows - success_count)}
            new_data.update(settings)
            ratio_csv_data.append(new_data)

    print(ratio_csv_data)

    new_df = pd.DataFrame(ratio_csv_data)
    if os.path.exists(ratio_file_dir):
        try:
            existing_df = pd.read_csv(ratio_file_dir)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True)
        except Exception as e:
            print(f"❌ error in open the file: {e}")
            combined_df = new_df
    else:
        print(f"💡 the file: {ratio_file_dir} doesn't exist, creating new one")
        combined_df = new_df


    combined_df.to_csv(ratio_file_dir, index=False, encoding='utf-8')
    return ratio_file_dir