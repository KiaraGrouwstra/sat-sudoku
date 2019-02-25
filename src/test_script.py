#Importing the Libraries
import os
import fetch
import sudoku

#Test Function
def convert_to_dimacs_string(sudoku_problems_list):
    sudoku_dimacs_string_list = []
    for sudoku_problem in sudoku_problems_list:
        s = []
        for (key, belief) in sudoku_problem:
            s.append(key + " 0\n")
        sudoku_dimacs_string_list.append(s)
    return sudoku_dimacs_string_list

# Test Code

#Fetching the sudoku problem(s)
file_name = fetch.get_sudoku('top91.sdk.txt')
with open(file_name) as f:
    sudoku_problems = f.readlines() #List of strings where each string is a sudoku problem of the form '.34..23..etc'

#Fetching the rules
file_name = fetch.get_sudoku('sudoku-rules.txt')
with open(file_name) as f:
    sudoku_rules = f.readlines()

#Converting from the '..32....' format to the dimacs string format '116 0\n 127 0\n...'
sudoku_problems = sudoku.parse_sudoku_lines(sudoku_problems) # List of List of Tuples [[(), (), ....]....[(), (), ....]]
sudoku_dimacs_string_list = convert_to_dimacs_string(sudoku_problems)
sudoku_full_problem_list = [''.join(sudoku_rules) + ''.join(sudoku_dimacs_string_list[i]) for i in range(len(sudoku_dimacs_string_list))]

#Writing to a file
open('output.out', 'w').close()
for i in range(len(sudoku_full_problem_list)):
    print(i+1)
    with open(fetch.get_sudoku('sudoku-example-full-test.out'), 'w') as f:
        f.write(sudoku_full_problem_list[i])
    os.system('python src/sat.py -p1 -S1 ./data/sudoku-example-full-test.out >> output.out')
    #os.system('python src/sat.py -p1 -S1 ./data/sudoku-example-full-test.out')

#Retrieving the output from the output file
with open(os.path.join(os.getcwd(), 'output.out')) as f:
    solved = f.readlines()
solved = [s[0:len(s)-1] == 'True' for s in solved]
if all(solved):
    print("All problems have been solved")
else:
    print(f"Solved:{solved.count(True)}, Unsolved: {solved.count(False)}")