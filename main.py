import sys
from bollinger_bands.bollinger_bands import bollinger_bands
from error_handle.log_crash import log_unhandled_exception
sys.excepthook = log_unhandled_exception

from min_max_pattern.find_pattern import min_max
from fastapi import FastAPI

app = FastAPI()

if __name__ == "__main__":
    # bollinger_bands()
    min_max()

# for creating .exe file use the command:
# pyinstaller --onefile --add-data ".env;." main.py
