import csv
from datetime import datetime
from itertools import chain

import date_functions

def create_output(starting_date: datetime, series_length: int, col_differences: list, col_null_fraction: list):
    col_dict = {}
    k = 0
    while k < len(col_differences):
        if k == 0:
            col_dict[k] = date_functions.generate_date_series_from_date(starting_date, col_differences[k], series_length)
        else:
            col_dict[k] = date_functions.generate_date_series_from_series(col_dict[k-1], col_differences[k])
        k += 1

    master_data = list(list(a) for a in zip(*col_dict.values()))

    master_data = date_functions.nullify_rows_date_cols(master_data, col_null_fraction)

    return master_data


def export_output(output, filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)
