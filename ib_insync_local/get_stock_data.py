from ib_insync import *
from config import settings

ib = IB()

ib.connect(settings.host, settings.demo_port, clientId=settings.client_id)

def get_stock_data(stock, end_data_time, duration_time, bar_size):
    curr_stock = Stock(stock, "SMART", "USD")

    if stock is None:
        print("Stock name not found")
        return None

    bars = ib.reqHistoricalData(
        curr_stock,
        endDateTime=end_data_time,
        durationStr=duration_time,
        barSizeSetting=bar_size,
        whatToShow='MIDPOINT',
        useRTH=True,
    )

    return util.df(bars)