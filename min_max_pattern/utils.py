

def check_deviation_down(row, local_min_max):
    return row["close"] < local_min_max or row["open"] < local_min_max

def check_deviation_up(row, local_min_max):
    return row["close"] > local_min_max or row["open"] > local_min_max

def sequence_ok(sequence_count, target):
    return sequence_count >= target

def chack_boundary(j, bound, indicate):
    j += -1 if indicate else 1
    return -1 if j < 0 or j >= bound else j

