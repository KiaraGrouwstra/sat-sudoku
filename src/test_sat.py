import numpy as np
import copy
import tempfile
import os
from collections import defaultdict
from fetch import *

# constants

U = 0
Y = 1
N = -1
eye = lambda x: x

# Necessary Helper Functions

def rev_enum(lst):
  '''reverse enumeration, so we can safely remove stuff without messing up our indices'''
  return list(enumerate(lst))[::-1]

assert rev_enum(['a','b']) == [(1, 'b'), (0, 'a')]

# def parse_dimacs(parse_fn):
#   def parse_lines(lines):
#     '''parse a DIMACS format file with facts based on a parser function, ignoring p/c lines and final 0s'''
#     rows = list(filter(lambda s: s[0] not in ['c', 'p', 'd'], lines))
#     result = [list(map(parse_fn, line.strip().split(' ')[:-1])) for line in rows]
#     return result
#   return parse_lines

# assert parse_dimacs(eye)(['123 -456 0']) == [['123', '-456']]

def read_file(file, parse_fn):
  '''read a file and parse its lines'''
  with open(file) as f:
    lines = f.readlines()
  return parse_fn(lines)

def parse_dimacs_dict(dimacs_file_contents):
  clause_dict = {}
  rows = list(filter(lambda s : s[0] not in ['c', 'p', 'd'], dimacs_file_contents))
  for i in range(len(rows)):
    temp_dict = {}
    term_list = rows[i].split(' ')
    del term_list[-1]
    for term in term_list:
      key = int(''.join(list(term)[1:])) if term[0] == '-' else int(term)
      temp_dict[key] = -1 if term[0] == '-' else 1
    clause_dict[i] = temp_dict
  return clause_dict

assert len(read_file(example_fn, parse_dimacs)) == 18

def write_dimacs(file, rules, ser_fn):
  '''write facts to a DIMACS format file based on a serialization function, incl. p/c lines and final 0s'''
  # TODO: p cnf max_variables clauses
#   max_variables = ???
#   clauses = len(rules)
#   header = f'p cnf {max_variables} {clauses}'
  s = '\n'.join(list(map(lambda ors: '\n'.join(list(map(lambda x: ('-' if x[1] == N else '') + ser_fn(x[0]), ors))) + ' 0', rules)))
  with open(file, 'w') as f:
    f.write(s)

tmp_file = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))
write_dimacs(tmp_file, [[(1, N)]], str)
assert read_file(tmp_file, parse_dimacs) == [['-1']]

def pick_guess_fact(rules, facts):
  '''pick a fact to guess. presume all known facts are pruned from rules (by simplify_initial), so only tally facts in rules.'''
  relevances = defaultdict(lambda: 0, {})
  for ors in rules:
    for rule in ors:
      (key, is_neg) = rule
      relevances[key] = relevances[key] + 1
  return max(relevances)

assert pick_guess_fact([[('123', Y)]], {}) == '123'

# TODO: dedupe logic with simplify
def simplify_initial(rules, facts):
  '''do a one-time clean-up of tautologous and pure-literal clauses.'''
  for (rules_idx, ors) in rev_enum(rules):

    # tautology: p or not p is redundant
    # TODO: handle cases where we have multiple instances of the same variable with the same beliefs
    # group beliefs by key
    res = {}
    for (key, belief) in ors:
      res.setdefault(key, []).append(belief)
    # check if any key has multiple (= complementing) beliefs
    if any(map(lambda arr: len(set(arr)) > 1, res.values())):
      # ditch fact
      # TODO: switch to linked list for constant-time deletions
      # TODO: or instead just create new list for the whole pass
      del rules[rules_idx]
      continue

    # clean out pure literals
    # TODO: properly implement pure literal removal, which actually means checking if a variable only has positive/negative occurrences left!
    # if only one option...
    if len(ors) == 1:
      [(key, belief)] = ors
      if facts[key] == -belief:  # opposite beliefs
        # clash detected, report it
        return (N, [], [])
      else:
        # consider it fact
        facts[key] = belief
      # we've exhausted the info in this rule, so get rid of it
      del rules[rules_idx]
      continue

  sat = U if len(rules) else Y
  return (sat, rules, facts)

assert simplify_initial([[('0', Y), ('1', N), ('0', N), ('0', N)], [('1', N)]], { '0':Y, '1':U })[1] == []

def simplify(rules, facts):
  '''simplify out unit clauses until we get stuck.
     returns (satisfiability, rules, facts).'''
  prev_left = 0
  rules_left = len(rules)
  while rules_left != prev_left:
    # print(f'{len(rules)} rules left')
    for (rules_idx, ors) in rev_enum(rules):
      for (ors_idx, rule) in rev_enum(ors):
        (key, belief) = rule
        # TODO: parallelize lookups with linalg
        fact = facts[key]
        if fact != U:  # if we know something about this fact...
          if belief == fact:
            # data agrees, OR rule satisfied, ditch whole rule
            del rules[rules_idx]
            break
          else:
            # data clashes, ditch option from rule
            del ors[ors_idx]
            # del rules[rules_idx][ors_idx]
            # if only one option remains...
            if len(ors) == 1:
              [(key, belief)] = ors
              if facts[key] == -belief:  # opposite beliefs
                # clash detected, report it
                return (N, [], [])
              else:
                # consider it fact
                facts[key] = belief
              # we've exhausted the info in this rule, so get rid of it
              del rules[rules_idx]
              break
            continue
        # else:  # no data available, nothing to do here
    prev_left = rules_left
    rules_left = len(rules)
  sat = U if rules_left else Y
  return (sat, rules, facts)

assert simplify([[(0, Y), (1, Y)]], { 0:Y, 1:U })[0] == Y
assert simplify([[(0, N), (1, N)]], { 0:Y, 1:Y })[0] == N
assert simplify([[(0, Y), (1, Y)]], { 0:U, 1:U })[0] == U

def split(rules_, facts_, facts_printer, fact_printer):
  '''guess a fact to proceed after simplify fails.'''
  rules = copy.deepcopy(rules_)
  facts = copy.deepcopy(facts_)

  guess_fact = pick_guess_fact(rules, facts)
  print_fact = fact_printer(guess_fact)
  guess_value = Y  # TODO: maybe also guess false?
  facts[guess_fact] = guess_value
  # print(f'guess     {print_fact}: {guess_value}')
  # print(facts_printer(facts))
  (sat, rules, facts) = simplify(rules, facts)

  if sat == U:
    (sat, rules, facts) = split(rules, facts, facts_printer, fact_printer)
  if sat == N:
    # clash detected, backtrack
    corrected = -guess_value  # opposite of guess
    facts_[guess_fact] = corrected
    # TODO: backtrack to assumption of clashing fact?
    # print(f'backtrack {print_fact}: {corrected}')
    # print(facts_printer(facts))
    (sat, rules, facts) = simplify(rules_, facts_)
    if sat == U:
      (sat, rules, facts) = split(rules, facts, facts_printer, fact_printer)
  return (sat, rules, facts)

assert split([[(0, N), (1, N)]], { 0:U, 1:U }, eye, eye)[0] == Y
