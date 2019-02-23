from dp import *

# stuff specific to our sudoku representation

# TODO: replace fact representation with a set, as that would work across problem types.
# complication: this means 123 and -123 are stored separately and we don't check for clashes here.
# instead remove variable instance from all rules, regarding empty clauses as clashes.

def parse_sudoku_line(sudoku):
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

assert parse_sudoku_line('5...68..........6..42.5.......8..9....1....4.9.3...62.7....1..9..42....3.8.......')[0][0] == ('004', Y)

def parse_sudoku_lines(lines):
  return list(map(parse_sudoku_line, lines))

def sudoku_board(facts):
  '''return a human-friendly 2D sudoku representation. works only after it's solved!
     find the most likely number for each tile, and convert back from index to digit (+1).'''
  ROWS = 9
  COLS = 9
  DIGITS = 9

  board = [[]] * ROWS
  for row in range(ROWS):
    board[row] = [0] * COLS

  for i in range(1,ROWS+1):
    for j in range(1,COLS+1):
      for k in range(1,DIGITS+1):
        key = int(f'{i}{j}{k}')
        if facts[key] == Y:
          board[i-1][j-1] = k
          break
  return '\n'.join([' '.join(map(str, l)) for l in board])

def_dict = defaultdict(lambda: U, {111: Y })
assert sudoku_board(def_dict)[0][0] == 1

def rules_to_dict(clauses, sudoku)
  '''merge rule dicts into a single dict for sudoku'''
  clause_list = [[(variable, belief) for variable, belief in clauses[outer_key].items()] for outer_key in clauses]
  example_sudoku_list = [[(variable, belief) for variable, belief in sudoku[outer_key].items()] for outer_key in sudoku]
  rules_list = clause_list + example_sudoku_list
  temp_dict_list = list(map(dict, rules_list))
  rules = {key : value for key, value in enumerate(temp_dict_list)}
  return rules

def solve_sudoku(clauses, sudoku, out_file, fact_printer=dict):
  rules = rules_to_dict(clauses, sudoku)
  return solve_csp(rules, out_file, fact_printer=dict)
