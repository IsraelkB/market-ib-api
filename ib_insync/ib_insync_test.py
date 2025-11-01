from ib_insync import *
from config import settings
import csv
from calculate_bollinger_bands import *
import os
from datetime import datetime, timedelta

ib = IB()

# # live trade conaction
# ib.connect(settings.host, settings.port, clientId=settings.client_id)
# paper connection
ib.connect(settings.host, settings.demo_port, clientId=settings.client_id)

stock_name = input("Enter stock name: ").upper()

stock = Stock(stock_name, "SMART", "USD")

if stock is None:
    raise ValueError("Stock name not found")

csv_file = f"C:/Users/Israel/PycharmProjects/market ib api/reports/{stock_name}_bars.csv"
os.makedirs(os.path.dirname(csv_file), exist_ok=True)

with open(csv_file, mode="w", newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["date", "open", "high", "low", "close", "volume",
                     "middle_band", "upper_1σ", "lower_1σ","upper_2σ", "lower_2σ",
                     "upper_3σ", "lower_3σ"])

    bars = ib.reqHistoricalData(
            stock,
            endDateTime='',
            durationStr="1 W",
            barSizeSetting='1 min',
            whatToShow='MIDPOINT',
            useRTH=True,
        )
    if not bars:
        print(f"⚠️ לא התקבלו נתונים עבור {stock}")
    else:
        df = util.df(bars)
        # df_pandas = util.df(bars)

        calculate_bollinger_bands(df)
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
                row['upper_3σ'], row['lower_3σ']
            ])

print(f"✅ סיום. כל הנתונים נשמרו בהצלחה בקובץ {stock_name}_bars.csv")