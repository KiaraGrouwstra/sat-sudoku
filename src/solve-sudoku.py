#!/usr/bin/python

from fetch import *
from sat import *
from sudoku import *

clauses = read_file(rule_fn, parse_dimacs)
example = read_file(example_fn, parse_dimacs)
print(solve_sudoku(clauses, example))