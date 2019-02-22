import numpy as np
import time
from sat import *

# stuff specific to our sudoku representation

ROWS = 9
COLS = 9
DIGITS = 9
# TODO: replace this ndarray representation with a set, as that would work across problem types.
# complication: this means 123 and -123 are stored separately and we don't check for clashes here.
# instead remove variable instance from all rules, regarding empty clauses as clashes.
SUDOKU_SHAPE = (ROWS, COLS, DIGITS)

def parse_sudoku(s):
  '''parse a sudoku fact like '-356' to ((row, col, digit), belief), numbers decremented by 1 to serve as indices'''
  belief = N if s[0] == '-' else Y
  if belief == N:
    s = s[1:]
  (row, col, digit) = list(map(int, list(s)))
  key = (row-1, col-1, digit-1)
  return (key, belief)

assert parse_sudoku('-356') == ((2, 4, 5), N)

def parse_sudoku_line(sudoku):
  clauses = []
  for i, char in enumerate(sudoku.strip()):
    if char != ".":
      row = i // 9
      col = i % 9
      digit = int(char) - 1
      key = (row, col, digit)
      tpl = (key, Y)
      clauses.append([tpl])
  return clauses

assert parse_sudoku_line('5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......')[0][0] == ((0,0,4), Y)

def parse_sudoku_lines(lines):
  return list(map(parse_sudoku_line, lines))

def sudoku_board(facts):
  '''return a human-friendly 2D sudoku representation. works only after it's solved!
     find the most likely number for each tile, and convert back from index to digit (+1).'''
  return np.multiply(np.max(facts, axis=2), (np.argmax(facts, axis=2) + 1))

assert sudoku_board(np.array([[[Y]]])) == np.array([[1]])

def print_fact(fact):
  (row, col, digit) = fact
  return (row+1, col+1, digit+1)

assert print_fact((0,0,0)) == (1,1,1)

def solve_sudoku(clauses, sudoku):
  start = time.time()

  # print('initialization')
  rules = clauses + sudoku
  facts = np.zeros(SUDOKU_SHAPE, dtype=np.short)  # initialize facts as U
  # print(sudoku_board(facts))

  # print('simplify init')
  (sat, rules, facts) = simplify_initial(rules, facts)
  # assert sat != N
  if sat == N:
    return False
  # print(sudoku_board(facts))

  # print('simplify')
  (sat, rules, facts) = simplify(rules, facts)
  # assert sat != N
  if sat == N:
    return False
  # print(sudoku_board(facts))

  # print('split to answer')
  if sat == U:
    (sat, rules, facts) = split(rules, facts, sudoku_board, print_fact)
  # assert sat != N
  if sat == N:
    return False

  print(f'took {time.time() - start} seconds')
  # print('final solution')
  print(sudoku_board(facts))

  # write_dimacs(tmp_file, [[((1,2,3), N)]], print_fact)
  return True
