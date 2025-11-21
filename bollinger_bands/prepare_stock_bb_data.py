from ib_insync import *
import csv
# from calculate_bollinger_bands import *
import os
from config import settings
from indecators.calculate_bollinger_bands import calculate_bollinger_bands
from indecators.calculate_ma import ma_100, ma_20, ma_50
from ib_insync_local.get_stock_data import get_stock_data


def run_ib_test(stock_settings, csv_file, stock):

    os.makedirs(os.path.dirname(csv_file), exist_ok=True)

    with open(csv_file, mode="w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["date", "open", "high", "low", "close", "volume",
                         "middle_band", "upper_1σ", "lower_1σ","upper_2σ", "lower_2σ",
                         "upper_3σ", "lower_3σ", "MA_100"])

        df = get_stock_data(stock, stock_settings["end_data_time"], stock_settings["duration_time"], stock_settings["bar_size"])
        if df is None:
            print(f"⚠️ לא התקבלו נתונים עבור {stock}")

        calculate_bollinger_bands(df)
        ma_20(df)
        # calculate_bollinger_bands_pandas(df_pandas)

        for _, row in df.iterrows():
            writer.writerow([
                row['date'],
                row['open'],
                row['high'],
                row['low'],
                row['close'],
                row['volume'],
                row['middle_band'],
                row['upper_1σ'], row['lower_1σ'],
                row['upper_2σ'], row['lower_2σ'],
                row['upper_3σ'], row['lower_3σ'],
                row['MA_100']
            ])

        return csv_file