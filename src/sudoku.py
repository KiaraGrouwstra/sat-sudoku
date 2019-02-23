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
<<<<<<< HEAD
  board = np.zeros((ROWS, COLS), dtype = np.int32)
=======

  board = [[]] * ROWS
  for row in range(ROWS):
    board[row] = [0] * COLS

>>>>>>> f64798b4f0084d052876252c2cbde8dd7105935c
  for i in range(1,ROWS+1):
    for j in range(1,COLS+1):
      for k in range(1,DIGITS+1):
        key = int(f'{i}{j}{k}')
        if facts[key] == Y:
          board[i-1][j-1] = k
          break
  return '\n'.join([' '.join(map(str, l)) for l in board])

<<<<<<< HEAD
def_dict = defaultdict(lambda: U, {111: Y })
assert sudoku_board(def_dict)[0][0] == 1

def solve_sudoku(clauses, sudoku):
  start = time.time()

  # print('initialization')
  # TODO Convert the rules into a dictionary containing the rules + sudoku_example
  rules = rules_to_dict(clauses, sudoku)
  facts = defaultdict(lambda: U, {})  # initialize facts as U
  #print(sudoku_board(facts))

  # print('simplify init')
  (sat, rules, facts) = simplify_initial(rules, facts)
  # assert sat != N
  if sat == N:
    return False
  #print(sudoku_board(facts))

  # print('simplify')
  (sat, rules, facts) = simplify(rules, facts)
  # assert sat != N
  if sat == N:
    return False
  #print(sudoku_board(facts))

  # print('split to answer')
  if sat == U:
    (sat, rules, facts) = split(rules, facts, sudoku_board, eye)
  # assert sat != N
  if sat == N:
    return False

  print(f'took {time.time() - start} seconds')
  # print('final solution')
  print(sudoku_board(facts))

  # write_dimacs(tmp_file, [[((1,2,3), N)]], eye)
  return True
=======
def_dict = defaultdict(lambda: U, { '111': Y })
assert sudoku_board(def_dict)[0][0] == '1'
>>>>>>> f64798b4f0084d052876252c2cbde8dd7105935c
