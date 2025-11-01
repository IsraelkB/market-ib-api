from ib_insync import *
from config import settings
import time
import csv
from datetime import datetime, timedelta

ib = IB()

# # live trade conaction
# ib.connect(settings.host, settings.port, clientId=settings.client_id)

# paper connection
ib.connect(settings.host, settings.demo_port, clientId=settings.client_id)
stock = Stock("NVDA", "SMART", "USD")

csv_file = "/report/nvda_bars.csv"


end_time = datetime.strptime("20251031 16:00:00", "%Y%m%d %H:%M:%S")
min_time = datetime.strptime("20251031 09:40:00", "%Y%m%d %H:%M:%S")

with open(csv_file, mode="w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["date", "open", "high", "low", "close", "volume", "Count", "WAP"])

    while end_time > min_time:
        bars = ib.reqHistoricalData(
            stock,
            endDateTime=end_time.strftime("%Y%m%d %H:%M:%S"),
            durationStr="6000 S",
            barSizeSetting='2 mins',
            whatToShow='MIDPOINT',
            useRTH=True,
            chartOptions=[TagValue("studyName", "BollingerBands")]
        )

        if not bars:
            print(f"⚠️ לא התקבלו נתונים עבור {end_time}")
        else:
            df = util.df(bars)
            for _, row in df.iterrows():
                writer.writerow([row['date'], row['open'], row['high'], row['low'], row['close'], row['volume'], row['Count'], row['WAP']])
            print(f"✅ נכתבו נתונים עד {end_time}")

        end_time -= timedelta(minutes=10)
        # time.sleep(2)

print("✅ סיום. כל הנתונים נשמרו בהצלחה בקובץ nvda_bars.csv")