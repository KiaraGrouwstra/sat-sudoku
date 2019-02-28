'''a script to convert sudokus from dot to dimacs format'''
import os
import glob
import logging
from sudoku import parse_sudoku_line

def main():
    '''run example sudokus'''
    data_path = os.path.join(os.getcwd(), 'data')
    dot_path = os.path.join(data_path, 'dot')
    dimacs_path = os.path.join(data_path, 'dimacs', 'sudoku')

    # Fetching the rules
    fpath = os.path.join(data_path, 'dimacs', 'sudoku-rules.txt')
    with open(fpath) as file:
        sudoku_rules = file.readlines()
    rules_str = ''.join(sudoku_rules)

    # sudoku_paths = glob.glob(os.path.join(dot_path, '*.txt'))
    sudoku_paths = ['/home/tycho/Downloads/Telegram Desktop/al_escargot.txt']
    for sudoku_path in sudoku_paths:
        # sudoku_type = os.path.basename(sudoku_path).split('.')[0]
        sudoku_type = 'janne'
        print(sudoku_type)

        # mkdir
        directory = os.path.join(dimacs_path, sudoku_type)
        if not os.path.exists(directory):
            os.makedirs(directory)

        # Fetching the sudoku problem(s)
        with open(sudoku_path) as file:
            # List of strings where each string is a sudoku problem of the form '.34..23..etc'
            sudoku_problems = file.readlines()

        for sudoku_problem in sudoku_problems:
            # convert from '..32....' to DIMACS '116 0\n 127 0\n...'
            # List of Tuples [(), (), ....]....[(), (), ....]
            sudoku_trimmed = sudoku_problem.strip()
            sudoku = parse_sudoku_line(sudoku_trimmed)
            sudoku_dimacs = [key + ' 0\n' for (key, _) in sudoku]
            sudoku_full = rules_str + ''.join(sudoku_dimacs)
            fpath = os.path.join(directory, f'sudoku-{sudoku_trimmed}-dimacs.in')
            with open(fpath, 'w') as file:
                file.write(sudoku_full)

if __name__ == "__main__":
    main()
