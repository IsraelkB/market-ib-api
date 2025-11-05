def sequence_ok(sequence_count, target):
    return sequence_count >= target

def chack_boundary(j, bound, indicate):
    j += -1 if indicate else 1
    return -1 if j < 0 or j >= bound else j

def init_min_max(row, start, end):
    min_row = row.copy()
    min_row["start_date"] = start
    min_row["end_date"] = end
    return min_row
