import traceback
from datetime import datetime
from utils_folder.get_path import get_base_path


def log_unhandled_exception(exc_type, exc_value, exc_traceback):
    root_path = get_base_path()
    log_file = f"{root_path}/error_handle/crash.log"
    with open(log_file, "a") as f:
        f.write("\n" + "="*80 + "\n")
        f.write(f"TIME: {datetime.now()}\n")
        f.write("UNHANDLED EXCEPTION:\n")
        f.write("".join(traceback.format_exception(exc_type, exc_value, exc_traceback)))
        f.write("\n")
