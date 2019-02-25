'''stuff specific to our sudoku representation'''
from dp import solve_csp, Y, U

# TODO: replace fact representation with a set? store 123/-123 separately.

def parse_sudoku_line(sudoku):
    '''parse a line like 234.23.43.2 to a list of clauses'''
    clauses = []
    for i, char in enumerate(sudoku.strip()):
        if char != ".":
            row = i // 9
            col = i % 9
            digit = int(char) - 1
            key = f'{row}{col}{digit}'
            tpl = (key, Y)
            clauses.append([tpl])
    return clauses

def parse_sudoku_lines(lines):
    '''parse sudoku lines like 3432.23.4322'''
    return list(map(parse_sudoku_line, lines))

def sudoku_board(facts):
    '''return a human-friendly 2D sudoku representation. works only after it's solved!
        find the most likely number for each tile, and convert back from index to digit (+1).'''
    rows = 9
    cols = 9
    digits = 9

    board = [[]] * rows
    for row in range(rows):
        board[row] = [0] * cols

    for i in range(1, rows+1):
        for j in range(1, cols+1):
            for k in range(1, digits+1):
                key = int(f'{i}{j}{k}')
                if facts.get(key, U) == Y:
                    board[i-1][j-1] = k
                    break
    return '\n' + '\n'.join([' '.join(map(str, l)) for l in board])

def rules_to_dict(clauses, sudoku):
    '''merge rule dicts into a single dict for sudoku'''
    clause_list = [[(variable, belief) for variable, belief in clauses[outer_key].items()]
                   for outer_key in clauses]
    example_sudoku_list = [[(variable, belief) for variable, belief in sudoku[outer_key].items()]
                           for outer_key in sudoku]
    rules_list = clause_list + example_sudoku_list
    temp_dict_list = list(map(dict, rules_list))
    rules = {key : value for key, value in enumerate(temp_dict_list)}
    return rules

def solve_sudoku(clauses, sudoku, out_file, fact_printer=dict):
    '''solve a sudoku given separate rules / game state'''
    rules = rules_to_dict(clauses, sudoku)
    return solve_csp(rules, out_file, fact_printer)
