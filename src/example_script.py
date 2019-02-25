'''a script to run the example sudokus to verify our algorithm'''
# Importing the Libraries
import os
from fetch import get_sudoku
from sudoku import parse_sudoku_lines

# Test Function
def convert_to_dimacs_string(sudoku_problems_list):
    '''convert a sudoku in dot format to dimacs format'''
    sudoku_dimacs_string_list = []
    for sudoku_problem in sudoku_problems_list:
        strn = []
        for (key, _) in sudoku_problem:
            strn.append(key + ' 0\n')
        sudoku_dimacs_string_list.append(strn)
    return sudoku_dimacs_string_list

# Test Code

def main():
    '''run example sudokus'''
    # Fetching the sudoku problem(s)
    file_name = get_sudoku('test_sudoku.out')
    with open(file_name) as file:
        # List of strings where each string is a sudoku problem of the form '.34..23..etc'
        sudoku_problems = file.readlines()

    # Fetching the rules
    file_name = get_sudoku('sudoku-rules.txt')
    with open(file_name) as file:
        sudoku_rules = file.readlines()

    # Converting from the '..32....' format to the dimacs string format '116 0\n 127 0\n...'
    # List of List of Tuples [[(), (), ....]....[(), (), ....]]
    sudoku_problems = parse_sudoku_lines(sudoku_problems)
    sudoku_dimacs_string_list = convert_to_dimacs_string(sudoku_problems)
    rules_str = ''.join(sudoku_rules)
    sudoku_full_problem_list = [rules_str + ''.join(sudoku) for sudoku in sudoku_dimacs_string_list]

    #Writing to a file
    open('output.out', 'w').close()
    for (i, sudoku_full_problem) in enumerate(sudoku_full_problem_list):
        print(i+1)
        with open(get_sudoku('sudoku-example-full-test.out'), 'w') as file:
            file.write(sudoku_full_problem)
        os.system('python src/sat.py -p -l2 -S1 ./data/sudoku-example-full-test.out >> output.out')
        # os.system('python src/sat.py -p -S1 ./data/sudoku-example-full-test.out')

    # Retrieving the output from the output file
    with open(os.path.join(os.getcwd(), 'output.out')) as file:
        solved = file.readlines()
    solved = [s[0:len(s)-1] == 'True' for s in solved]
    if all(solved):
        print("All problems have been solved")
    else:
        print(f"Solved:{solved.count(True)}, Unsolved: {solved.count(False)}")

if __name__ == "__main__":
    main()
