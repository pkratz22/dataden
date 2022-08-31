import csv
from datetime import date
from random import seed

from . import related_date_functions, separate_column_functions

def create_date_output(starting_date: date, series_length: int, col_differences: list, col_null_fraction: list, **kwargs):
    seed_number = kwargs.get('seed', None)
    if seed_number is not None:
        seed(seed_number)
    
    col_dict = {}
    k = 0
    while k < len(col_differences):
        if k == 0:
            col_dict[k] = related_date_functions.generate_date_series_from_date(starting_date, col_differences[k], series_length)
        else:
            col_dict[k] = related_date_functions.generate_date_series_from_series(col_dict[k-1], col_differences[k])
        k += 1

    master_data = list(list(a) for a in zip(*col_dict.values()))

    master_data = related_date_functions.nullify_rows_date_cols(master_data, col_null_fraction)
    return master_data


def get_column(current_list: list, position_to_extract: int):
    if position_to_extract > len(current_list[0]):
        position_to_extract = len(current_list[0]) - 1
    elif position_to_extract < 0:
        position_to_extract = 0
    return [row[position_to_extract] for row in current_list]


def insert_column(current_list: list, new_list: list, insert_pos: int):
    return [a[:insert_pos]+[x]+a[insert_pos:] for a,x in zip(current_list, new_list)]


def insert_non_date_columns(current_list: list, position_of_column_to_match_nulls: int, position_to_insert: int, datatype: str, **kwargs):
    column_to_match_nulls = get_column(current_list, position_of_column_to_match_nulls)
    new_col = separate_column_functions.create_non_date_col(datatype, column_to_match_nulls, **kwargs)
    result = insert_column(current_list, new_col, position_to_insert)
    return result


def export_output(output, filename):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(output)
