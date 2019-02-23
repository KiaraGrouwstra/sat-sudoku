from sudoku import *

def test_parse_sudoku_line():
  assert parse_sudoku_line('5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......')[0][0] == ('004', Y)

def test_sudoku_board():
  def_dict = defaultdict(lambda: U, {111: Y })
  assert sudoku_board(def_dict)[0][0] == '1'
