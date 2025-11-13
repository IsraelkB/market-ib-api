import sys
from pathlib import Path

def get_path():
    if getattr(sys, "frozen", False):
        return Path(sys._MEIPASS)
    else:
        return Path(__file__).resolve().parent.parent

