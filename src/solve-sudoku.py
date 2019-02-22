#!/usr/bin/python

from fetch import *
from sat import *
from sudoku import *

clauses = read_file(rule_fn, parse_dimacs(parse_sudoku))
example = read_file(example_fn, parse_dimacs(parse_sudoku))

solve_sudoku(clauses, example)
