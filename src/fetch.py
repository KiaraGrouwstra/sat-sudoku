'''load test sudokus'''
import os

# Fetching the sudoku rules and a given example sudoku problem

def get_sudoku(fname):
    '''confirm a file exists and yield its path'''
    path = os.path.join(os.getcwd(), 'data', fname)
    assert os.path.isfile(path)
    return path

FILES = ('sudoku-rules.txt', 'sudoku-example.txt', '1000-sudokus.txt', 'damnhard.sdk.txt',
         'subig20.sdk.txt', 'top100.sdk.txt', 'top2365.sdk.txt', 'top870.sdk.txt', 'top91.sdk.txt',
         'top95.sdk.txt')
(RULE_FN, EXAMPLE_FN, ONEK_FN, DAMNHARD_GET_SUDOKUFN, SUBIG_FN, TOP100_FN, TOP2365_FN, TOP870_FN,
 TOP91_FN, TOP95_FN) = list(map(get_sudoku, FILES))
