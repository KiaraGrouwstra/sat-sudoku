import urllib.request
import os

# Fetching the sudoku rules and a given example sudoko problem

def get_sudoku(fname):
    path = os.getcwd() + '\\' + fname
    assert os.path.isfile(path)
    return path

files = ('sudoku-rules.txt', 'sudoku-example.txt', '1000-sudokus.txt', 'damnhard.sdk.txt', 'subig20.sdk.txt', 'top100.sdk.txt', 'top2365.sdk.txt', 'top870.sdk.txt', 'top91.sdk.txt', 'top95.sdk.txt')
(rule_fn, example_fn, onek_fn, damnhard_fn, subig_fn, top100_fn, top2365_fn, top870_fn, top91_fn, top95_fn) = list(map(get_sudoku, files))
