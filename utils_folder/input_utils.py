def collect_user_settings(*setting_names):
    user_input = {}
    param = input(f"please enter the sample values for:")
    for value in setting_names:
        param = input(f"\t{value}\n")
        user_input[value] = param

    return user_input

def collect_bb_settings():
    print("please enter the bb settings")
    sigma_multiplier = get_validated_int("please insert the mult σ you want\n", 1, 3)
    stop_loss_mode = get_validated_int("please insert the number of stp loss policy you want: 0- min/max, 1- candle\n",
                                       0, 1)
    min_bb_break_percent = get_validated_float(
        "please insert the min percentage (from the stock price) above/below the bb line\n",
        0, 1) * 0.01
    min_delay_after_loss = get_validated_int("please insert the time in minutes to delay after unsuccessful trade\n",
                                             0,60)
    get_in_reverse_candle = get_validated_int("do you want exam deals that the candle you trade is against the side? 1 for yes 0 for no\n",
                                              0,1)
    return {"sigma_multiplier": sigma_multiplier, "stop_loss_mode": stop_loss_mode, "min_bb_break_percent": min_bb_break_percent,
            "min_delay_after_loss": min_delay_after_loss, "get_in_reverse_candle": get_in_reverse_candle}

def collect_stock_settings():
    print("please enter the stock settings:")
    stock_name = input("Enter stock name:\n").upper()
    bar_size = input(
        "Enter bar size. Time period of one bar. Must be one of:\n\t'1 secs', '5 secs', '10 secs' 15 secs', '30 secs',"
        "'1 min', '2 mins', '3 mins', '5 mins', '10 mins', '15 mins', '20 mins', '30 mins', '1 hour', '2 hours', "
        "'3 hours', '4 hours', '8 hours','1 day', '1 week', '1 month'.\n").upper()
    duration_time = input("Enter duration time: Examples: '60 S', '30 D', '13 W', '6 M', '10 Y'.").upper()
    end_data_time = input("click enter to indicate the current time, or it can be given as a datetime.date or "
                          "datetime.datetime, or it can be given as a string in 'yyyyMMdd HH:mm:ss' format."
                          "If no timezone is given then the TWS login timezone is used.\n")
    return {"stock_name": stock_name, "bar_size": bar_size, "end_data_time": end_data_time, "duration_time": duration_time}

def get_validated_int(explain_str, min_val, max_val):
    while True:
        user_input = input(explain_str)
        try:
            user_input = int(user_input)
        except ValueError:
            print(f"please insert a valid number between {min_val} and {max_val}")
            continue

        if user_input < min_val or user_input > max_val:
            print(f"please insert a valid number between {min_val} and {max_val}")
            continue

        return user_input

def get_validated_float(explain_str, min_val, max_val):
    while True:
        user_input = input(explain_str)
        try:
            user_input = float(user_input)
        except ValueError:
            print(f"please insert a valid number between {min_val} and {max_val}")
            continue

        if user_input < min_val or user_input > max_val:
            print(f"please insert a valid number between {min_val} and {max_val}")
            continue

        return user_input