#!/usr/bin/python

from fetch import *
from sat import *
from sudoku import *

clauses = read_file(rule_fn, parse_dimacs(parse_fact))
example = read_file(example_fn, parse_dimacs(parse_fact))

assert solve_csp(clauses + example, sudoku_board)
