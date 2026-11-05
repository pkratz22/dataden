# dataden

Developed to create mock data for dates in a sequential process.

For example, if a company has a program that has four steps, it will create date data in sequential order.
It also allows users to indicate that a percentage of a column should be null (to account for the sequential data never reaching the last step).

## Installation

```
pip install -e .
```

## Usage

```python
from datetime import date
from dataden import dataden

d = dataden()
d.create_related_date_output(
    starting_date=date(2022, 1, 1),
    series_length=5,
    col_differences=[400, 30, 30, 10],      # max days after the previous column
    col_null_fraction=[0, 0, .5, .5],       # fraction of each column left null
    seed=1,
)
d.create_headers(['Enrollment Date', 'Kit Ship Date', 'Kit Return Date', 'Results Available Date'])
d.export_output('crm_test.csv')
```

Example output:

```
Enrollment Date,Kit Ship Date,Kit Return Date,Results Available Date
2022-03-10,2022-03-13,2022-04-02,2022-04-09
2022-10-19,2022-11-03,NaT,NaT
2023-01-27,2023-02-20,NaT,NaT
2022-02-02,2022-02-16,NaT,NaT
2022-05-11,2022-05-26,NaT,NaT
```

## Tests

```
pip install -e ".[test]"
pytest
```
