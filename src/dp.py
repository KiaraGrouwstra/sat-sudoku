'''generic functions related to Davis-Putnam not specific to sudoku'''
import copy
import time
from collections import defaultdict
import pickle

# constants

U = 0
Y = True
N = False
EYE = lambda x: x

# classes

class State:
    '''container for our solver state'''
    rules: dict
    facts: dict
    occurrences: dict

    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts
        self.occurrences = {belief: get_occurrences(rules, belief) for belief in [Y, N]}

# Necessary Helper Functions

def parse_dimacs(dimacs_file_contents):
    '''parse a dimacs file to rules (dict of dicts)'''
    clause_dict = {}
    rows = list(filter(lambda s: s[0] not in ['c', 'p', 'd'], dimacs_file_contents))
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

def read_file(path):
    '''read a file and parse its lines'''
    with open(path) as file:
        lines = file.readlines()
    return parse_dimacs(lines)

def write_dimacs(path, facts, ser_fn=str):
    '''write facts to a DIMACS format file based on a serialization function, incl. final 0s'''
    strn = '\n'.join([f'{"-" if v == N else ""}{ser_fn(k)} 0' for k, v in facts.items() if v != U])
    with open(path, 'w') as file:
        file.write(strn)

def pick_guess_fact(rules):
    '''pick a fact to guess. presume all known facts are pruned, so only tally facts in rules.'''
    relevances = defaultdict(lambda: 0, {})
    for ors in rules.values():
        for key in ors:
            relevances[key] += 1
    return max(relevances)

# TODO: dedupe logic with simplify
def simplify_initial(state):
    '''do a one-time clean-up of tautologies and pure-literal clauses.'''
    temp_rules = copy.copy(state.rules)
    for (rules_idx, ors) in temp_rules.items():

        res = {}
        for (key, belief) in ors.items():
            # clean out unit clauses
            # TODO: properly implement pure literal removal
            # if only one option...
            if len(ors) == 1:
                [(key, belief)] = list(ors.items())
                y = state.facts.get(key, U)
                if ((y == Y and belief == N) or (y == N and belief == Y)):    # opposite beliefs
                    # clash detected, report it
                    return (N, state)
                # consider it fact
                state.facts[key] = belief
                # TODO: to_remove.add(guess_fact)
                # we've exhausted the info in this rule, so get rid of it
                del state.rules[rules_idx]
                # occs = state.occurrences[belief].get(key, set())
                # occs.remove(rules_idx)
                # TODO: if not occs: check other belief, if both empty ditch both,
                # if other exists, trigger pure literal clause, setting the belief to that other value
                continue

    sat = U if state.rules else Y
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
        temp_rules = copy.copy(state.rules)
        for (rules_idx, ors) in temp_rules.items():
            temp_clause = copy.copy(ors)
            for (inner_key, belief) in temp_clause.items():
                # TODO: parallelize lookups with linalg
                fact = state.facts.get(inner_key, U)
                if fact != U:    # if we know something about this fact...
                    if belief == fact:
                        # data agrees, OR rule satisfied, ditch whole rule
                        del state.rules[rules_idx]
                        break
                    else:
                        # data clashes, ditch option from rule
                        del ors[inner_key]
                        # occs = state.occurrences[belief].get(inner_key, set())
                        # occs.remove(rules_idx)
                        # TODO: if not occs: check other belief,
                        # if both empty ditch both, if other exists,
                        # trigger pure literal clause, setting the belief to that other value
                        # del state.rules[rules_idx][ors_idx]
                        # if only one option remains...
                        if len(ors) == 1:
                            [(key, belief)] = list(ors.items())
                            y = state.facts.get(key, U)
                            if ((y == Y and belief == N) or (y == N and belief == Y)):    # opposite beliefs
                                # clash detected, report it
                                return (N, state)
                            # consider it fact
                            state.facts[key] = belief
                            # TODO: to_remove.add(guess_fact)
                            # we've exhausted the info in this rule, so get rid of it
                            del state.rules[rules_idx]
                            break
                        continue
                # else:    # no data available, nothing to do here
        prev_left = rules_left
        rules_left = len(state.rules)
    sat = U if rules_left else Y
    return (sat, state)

def split(state_, facts_printer, fact_printer):
    '''guess a fact to proceed after simplify fails.'''
    state = pickle.loads(pickle.dumps(state_, -1))

    guess_fact = pick_guess_fact(state.rules)
    print_fact = fact_printer(guess_fact)
    guess_value = Y  # TODO: maybe also guess false?
    state.facts[guess_fact] = guess_value
    # TODO: to_remove.add(guess_fact)
    print(f'guess     {print_fact}: {guess_value}')
    # print(facts_printer(facts))
    (sat, state) = simplify(state)

    if sat == U:
        (sat, state) = split(state, facts_printer, fact_printer)
    if sat == N:
        # clash detected, backtrack
        corrected = N if guess_value == Y else Y if guess_value == N else U  # opposite of guess
        state_.facts[guess_fact] = corrected
        # TODO: backtrack to assumption of clashing fact?
        print(f'backtrack {print_fact}: {corrected}')
        # print(facts_printer(state.facts))
        (sat, state) = simplify(state_)
        if sat == U:
            (sat, state) = split(state, facts_printer, fact_printer)
    return (sat, state)

def get_occurrences(rules, belief):
    '''get rule occurrences for a belief, e.g. { 123: set([3, 10]) }'''
    belief_occurrences = {}
    for line, ors in rules.items():
        for key, val in ors.items():
            if val == belief:
                belief_occurrences.get(key, set()).add(line)
    return belief_occurrences

def solve_csp(rules, out_file, fact_printer=dict):
    '''solve a general CSP problem and write its solution to a file. returns satisfiability.'''
    start = time.time()

    # print('initialization')
    # initialize facts as U
    facts = {}
    # print(fact_printer(facts))
    state = State(rules, facts)
    # occurrences = {belief: get_occurrences(rules, belief) for belief in [Y, N]}
    # state = State(rules, facts, occurrences)

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
        (sat, state) = split(state, fact_printer, EYE)
    # assert sat != N
    if sat == N:
        return False

    print(f'took {time.time() - start} seconds')
    # print('final solution')
    print(fact_printer(state.facts))

    # output DIMACS file 'filename.out' with truth assignments, TODO: empty if inconsistent.
    write_dimacs(out_file, state.facts)

    return sat == Y
