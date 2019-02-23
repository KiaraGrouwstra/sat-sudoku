import copy
import tempfile
import os
import time
from collections import defaultdict
from dataclasses import dataclass

# constants

U = 0
Y = 1
N = -1
eye = lambda x: x

# data classes

@dataclass
class State:
  rules: dict
  facts: dict
  occurrences: dict

# Necessary Helper Functions

def parse_dimacs(dimacs_file_contents):
  '''parse a dimacs file to rules (dict of dicts)'''
  clause_dict = {}
  rows = list(filter(lambda s : s[0] not in ['c', 'p', 'd'], dimacs_file_contents))
  for i in range(len(rows)):
    temp_dict = {}
    tautology = False
    term_list = rows[i].split(' ')[:-1]
    for term in term_list:
      is_neg = term[0] == '-'
      key = int(term[1:]) if is_neg else int(term)
      val = N if is_neg else Y
      if key not in temp_dict:
        temp_dict[key] = val
      else:
        if temp_dict[key] == val:
          continue
        else:
          tautology = True
          break
    if not tautology:
      clause_dict[i] = temp_dict
  return clause_dict

def read_file(file):
  '''read a file and parse its lines'''
  with open(file) as f:
    lines = f.readlines()
  return parse_dimacs(lines)

def write_dimacs(file, facts, ser_fn=str):
  '''write facts to a DIMACS format file based on a serialization function, incl. final 0s'''
  s = '\n'.join([f'{"-" if v == N else ""}{ser_fn(k)} 0' for k,v in facts.items() if v != U])
  with open(file, 'w') as f:
    f.write(s)

def pick_guess_fact(rules):
  '''pick a fact to guess. presume all known facts are pruned from rules (by simplify_initial), so only tally facts in rules.'''
  relevances = defaultdict(lambda: 0, {})
  for rules_idx, ors in rules.items():
    for inner_key, belief in ors.items():
      (key, is_neg) = (inner_key, belief)
      relevances[key] += 1
  return max(relevances)

# TODO: dedupe logic with simplify
def simplify_initial(state):
  '''do a one-time clean-up of tautologies and pure-literal clauses.'''
  temp_rules = copy.copy(state.rules)
  for (rules_idx, ors) in temp_rules.items():

    # clean out unit clauses
    # TODO: properly implement pure literal removal, which actually means checking if a variable only has positive/negative occurrences left!
    # if only one option...
    if len(ors) == 1:
      [(key, belief)] = list(ors.items())
      if state.facts[key] == -belief:  # opposite beliefs
        # clash detected, report it
        return (N, state)
      else:
        # consider it fact
        state.facts[key] = belief
        # TODO: to_remove.add(guess_fact)
      # we've exhausted the info in this rule, so get rid of it
      del state.rules[rules_idx]
      state.occurrences[belief][key].remove(rules_idx)
      # TODO: if not len(occurrences[belief][key]): check other belief, if both empty ditch both, if other exists, trigger pure literal clause, setting the belief to that other value
      continue

  sat = U if len(state.rules) else Y
  return (sat, state)

def simplify(state):
  '''simplify out unit clauses until we get stuck.
     returns (satisfiability, rules, facts).'''
  prev_left = 0
  rules_left = len(state.rules)

  # TODO: instead of deletes create new list for the whole pass?
  # TODO: do not full iterations but grab from to_remove
  while rules_left != prev_left:
    # print(f'{len(rules)} rules left')
    temp_rules = copy.copy(rules)
    for (rules_idx, ors) in temp_rules.items():
      temp_clause = copy.copy(ors)
      for (inner_key, belief) in temp_clause.items():
        # TODO: parallelize lookups with linalg
        fact = state.facts[inner_key]
        if fact != U:  # if we know something about this fact...
          if belief == fact:
            # data agrees, OR rule satisfied, ditch whole rule
            del state.rules[rules_idx]
            break
          else:
            # data clashes, ditch option from rule
            del ors[inner_key]
            state.occurrences[belief][inner_key].remove(rules_idx)
            # TODO: if not len(state.occurrences[belief][key]): check other belief, if both empty ditch both, if other exists, trigger pure literal clause, setting the belief to that other value
            # del state.rules[rules_idx][ors_idx]
            # if only one option remains...
            if len(ors) == 1:
              [(key, belief)] = list(ors.items())
              if state.facts[key] == -belief:  # opposite beliefs
                # clash detected, report it
                return (N, state)
              else:
                # consider it fact
                facts[key] = belief
                # TODO: to_remove.add(guess_fact)
              # we've exhausted the info in this rule, so get rid of it
              del state.rules[rules_idx]
              break
            continue
        # else:  # no data available, nothing to do here
    prev_left = rules_left
    rules_left = len(state.rules)
  sat = U if rules_left else Y
  return (sat, state)

def split(state_, facts_printer, fact_printer):
  '''guess a fact to proceed after simplify fails.'''
  state = copy.deepcopy(state_)

  guess_fact = pick_guess_fact(state.rules)
  print_fact = fact_printer(guess_fact)
  guess_value = Y  # TODO: maybe also guess false?
  state.facts[guess_fact] = guess_value
  # TODO: to_remove.add(guess_fact)
  # print(f'guess     {print_fact}: {guess_value}')
  # print(facts_printer(facts))
  (sat, state) = simplify(state)

  if sat == U:
    (sat, state) = split(state, facts_printer, fact_printer)
  if sat == N:
    # clash detected, backtrack
    corrected = -guess_value  # opposite of guess
    facts_[guess_fact] = corrected
    # TODO: backtrack to assumption of clashing fact?
    # print(f'backtrack {print_fact}: {corrected}')
    # print(facts_printer(state.facts))
    (sat, state) = simplify(state_)
    if sat == U:
      (sat, state) = split(state, facts_printer, fact_printer)
  return (sat, state)

def get_occurrences(rules, belief):
  '''get rule occurrences for a belief, e.g. { 123: set([3, 10]) }'''
  belief_occurrences = defaultdict(lambda: set())
  for line, ors in rules.items():
    for k, v in ors.items():
      if v == belief:
        belief_occurrences[k].add(line)

def solve_csp(rules, out_file, fact_printer=dict):
  start = time.time()

  # print('initialization')
  # initialize facts as U
  facts = defaultdict(lambda: U, {})
  # print(fact_printer(facts))
  occurrences = { belief: get_occurrences(rules, belief) for belief in [Y, N] }
  state = State(rules, facts, occurrences)

  # print('simplify init')
  (sat, state) = simplify_initial(state)
  # assert sat != N
  if sat == N:
    return False
  # print(fact_printer(state.facts))

  # print('simplify')
  (sat, state) = simplify(state)
  # assert sat != N
  if sat == N:
    return False
  # print(fact_printer(state.facts))

  # print('split to answer')
  if sat == U:
    (sat, state) = split(state, fact_printer, eye)
  # assert sat != N
  if sat == N:
    return False

  print(f'took {time.time() - start} seconds')
  # print('final solution')
  print(fact_printer(state.facts))

  # This output should again be a DIMACS file, but containing only the truth assignment to all variables (729 for Sudoku, different for other SAT problems). If your input file is called 'filename', then make sure your outputfile is called 'filename.out'. If there is no solution (inconsistent problem), the output can be an empty file. If there are multiple solutions (eg. non-proper Sudoku) you only need to return a single solution.
  write_dimacs(out_file, state.facts)

  return sat == Y
