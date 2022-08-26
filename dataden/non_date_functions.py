from random import choices, randint, seed
import string

import pandas as pd


def generate_string(string_length: int, lower_allowed: bool, upper_allowed: bool, numeric_allowed: bool, special_allowed: bool):
    if not (lower_allowed or upper_allowed or numeric_allowed or special_allowed):
        return None
    chars_allowed = ''
    if lower_allowed:
        chars_allowed += string.ascii_lowercase
    if upper_allowed:
        chars_allowed += string.ascii_uppercase
    if numeric_allowed:
        chars_allowed += string.digits
    if special_allowed:
        chars_allowed += '!$%^&*.,@#/?'
    return ''.join(choices(chars_allowed, k=string_length))

def generate_int(min_val: int, max_val: int):
    return randint(min_val, max_val)

def create_non_date_col(datatype: str, col_relation: list, **kwargs):
    """
    Create list of non-date data.
    Datatype options:
        'character string':
            default is lowercase characters
            can include:
                upper_allowed = True
                numeric_allowed = True
                special_allowed = True
        'int'
    """
    
    default_string_length = 10
    string_length = kwargs.get('string_length', default_string_length)
    seed_number = kwargs.get('seed', None)
    if datatype == 'string':
        lower_allowed = kwargs.get('lower_allowed', True)
        upper_allowed = kwargs.get('upper_allowed', False)
        numeric_allowed = kwargs.get('numeric_allowed', False)
        special_allowed = kwargs.get('special_allowed', False)
    elif datatype == 'int':
        lower_bound = kwargs.get('lower_bound', 0)
        upper_bound = kwargs.get('upper_bound', 0)
        if lower_bound > upper_bound:
            lower_bound, upper_bound = upper_bound, lower_bound
    if seed_number is not None:
        seed(seed_number)

    new_field = [None] * len(col_relation)

    for i in range(len(col_relation)):
        if pd.isnull(col_relation[i]):
            new_field[i] = None
            continue
        if datatype == 'string':
            new_field[i] = generate_string(string_length, lower_allowed, upper_allowed, numeric_allowed, special_allowed)
        elif datatype == 'int':
            new_field[i] = generate_int(lower_bound, upper_bound)
    return new_field
