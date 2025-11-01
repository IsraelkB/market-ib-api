from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from time import sleep
from ib_insync.config import settings
from threading import Thread

class TradeApp(EWrapper, EClient): 
    def __init__(self): 
        EClient.__init__(self, self)


if __name__ == '__main__':
    app = TradeApp()

    host = settings.host
    # port 7496 for live trading, 7497 is for paper trading
    port = settings.port
    client_id = settings.client_id

    app.connect(host, port, client_id)
    sleep(1)

    app_thread = Thread(target=app.run, daemon=True)
    app_thread.start()
    app.run()