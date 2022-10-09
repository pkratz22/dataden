import csv
from datetime import date
from random import seed
import related_date_functions
import separate_column_functions



class InputLogicError(Exception):
    def __init__(self, message):
        super().__init__(message)


class InputTypeError(Exception):
    def __init__(self, message):
        super().__init__(message)


class dataden():
    def __init__(self, data=None):
        if data is None:
            self.data = []
        elif isinstance(data, list):
            self.data = data
        else:
            raise InputTypeError("Data must be a list.")
        self.nrows = len(self.data)
        if len(self.data) > 0 and isinstance(self.data[0], list):
            self.ncols = len(self.data[0])
        else:
            self.ncols = 0
        self.headers = None

    def export_output(self, filename, **kwargs):
        subset = kwargs.get('subset', None)
        output = self.data
        if self.headers:
            output.insert(0, self.headers)
        if subset:
            output_subset = []
            for row in output:
                output_subset.append([row[i] for i in subset])
        with open(filename, "w") as f:
            writer = csv.writer(f)
            if subset:
                writer.writerows(output_subset)
            else:
                writer.writerows(output)
        if self.headers:
            self.data = self.data[1:]

    def create_related_date_output(self, starting_date: date, series_length: int, col_differences: list, col_null_fraction: list, **kwargs):
        date_format = kwargs.get('date_format', '%Y-%m-%d')

        seed_number = kwargs.get('seed', None)
        if seed_number is not None:
            seed(seed_number)

        if len(col_differences) != len(col_null_fraction):
            raise InputLogicError("Length of Col Differences and length of Col Null Fraction do not match")

        col_dict = {}
        k = 0
        while k < len(col_differences):
            if k == 0:
                col_dict[k] = related_date_functions.generate_date_series_from_date(starting_date, col_differences[k], series_length)
            else:
                col_dict[k] = related_date_functions.generate_date_series_from_series(col_dict[k-1], col_differences[k])
            k += 1

        self.data = list(list(a) for a in zip(*col_dict.values()))

        self.data = [[ind_date.strftime(date_format) for ind_date in date_row]
                     for date_row in self.data]

        self.data = related_date_functions.nullify_rows_date_cols(self.data, col_null_fraction)
        self.nrows = series_length
        self.ncols = len(col_differences)
        return self

    def get_column(self, position_to_extract: int):
        if position_to_extract > self.ncols:
            position_to_extract = self.ncols - 1
        elif position_to_extract < 0:
            position_to_extract = 0
        return [row[position_to_extract] for row in self.data]

    def insert_column(self, new_list: list, insert_pos: int):
        if not self.data:
            self.data = new_list
            self.ncols = 1
            self.nrows = len(new_list)
            return self
        if not isinstance(self.data[0], list):
            if insert_pos <= 0:
                self.data = [list(l) for l in zip(new_list, self.data)]
            else:
                self.data = [list(l) for l in zip(self.data, new_list)]
        else:
            self.data = [a[:insert_pos]+[x]+a[insert_pos:] for a,x in
                         zip(self.data, new_list)]
        return self

    def insert_individual_columns(self, position_of_column_to_match_nulls: int, position_to_insert: int, num_rows: int, datatype: str, **kwargs):
        if self.data:
            column_to_match_nulls = self.get_column(position_of_column_to_match_nulls)
            self.ncols += 1
        else:
            column_to_match_nulls = ['a'] * num_rows # only used to create column, data won't be used, which is why we use the temporary data 'a'
            self.ncols = 1
            self.nrows = num_rows
        new_col = separate_column_functions.create_individual_col(datatype, column_to_match_nulls, **kwargs)
        self.insert_column(new_col, position_to_insert)
        return self

    def create_headers(self, col_names: list):
        if not isinstance(col_names, list):
            raise InputTypeError("Column headers should be a list")
        if self.ncols != len(col_names):
            raise InputLogicError(
                "Number of columns is {ncols}, but number of column names is {nheaders}.".format(
                    ncols=self.ncols,
                    nheaders=len(col_names),
                ),
            )
        self.headers = col_names
        return self


def main():
    return 1

if __name__ == '__main__':
    main()
