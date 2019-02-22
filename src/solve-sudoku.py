#!/usr/bin/python

from fetch import *
from sat import *
from sudoku import *

clauses = read_file(rule_fn)
example = read_file(example_fn)

assert solve_csp(clauses + example, sudoku_board)
