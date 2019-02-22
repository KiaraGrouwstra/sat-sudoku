import urllib.request
import os.path

# Fetching the sudoku rules and a given example sudoko problem

def get_sudoku(fname):
    gist = 'https://gist.githubusercontent.com/tycho01/7fa87cf7b434fc6ab089113a7d70b323/raw/f2598208ef39effe52af8b269a0a414283e8f94d/'
    path = './data/' + fname
    if os.path.isfile(path):
        # print(path)
        return path
    else:
        (fn, msg) = urllib.request.urlretrieve(gist + fname, fname)
        print(fn)
        print(msg)
        return fn

files = ('sudoku-rules.txt', 'sudoku-example.txt', '1000-sudokus.txt', 'damnhard.sdk.txt', 'subig20.sdk.txt', 'top100.sdk.txt', 'top2365.sdk.txt', 'top870.sdk.txt', 'top91.sdk.txt', 'top95.sdk.txt')
(rule_fn, example_fn, onek_fn, damnhard_fn, subig_fn, top100_fn, top2365_fn, top870_fn, top91_fn, top95_fn) = list(map(get_sudoku, files))
