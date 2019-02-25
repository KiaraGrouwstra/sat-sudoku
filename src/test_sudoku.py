'''test sudoku functions'''
from collections import defaultdict
from dp import Y, U
from sudoku import parse_sudoku_line, sudoku_board

def test_parse_sudoku_line():
    '''test'''
    line = '5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......'
    assert parse_sudoku_line(line)[0][0] == '115'

def test_sudoku_board():
    '''test'''
    def_dict = defaultdict(lambda: U, {111: Y})
    assert sudoku_board(def_dict)[1][0] == '1'
