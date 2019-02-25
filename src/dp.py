'''generic functions related to Davis-Putnam not specific to sudoku'''
import time
import logging
from collections import defaultdict
import random
import pickle

# constants

U = 0
Y = 1
N = -1
EYE = lambda x: x

# classes

class State:
    '''container for our solver state'''
    rules: dict
    facts: dict
    occurrences: dict
    due_pure: set
    due_unit: set

    def __init__(self, rules):
        self.rules = rules
        self.facts = {}
        occ = {belief: get_occurrences(rules, belief) for belief in [Y, N]}
        self.occurrences = occ
        y_idxs = set(occ[Y].keys())
        n_idxs = set(occ[N].keys())
        self.due_pure = y_idxs.union(n_idxs) - y_idxs.intersection(n_idxs)
        self.due_unit = {line for line, ors in rules.items() if len(ors) == 1}

# Necessary Helper Functions

def add_fact(state, var, belief):
    '''add a fact'''
    assert belief != U
    state.facts[var] = belief
    for fact in [Y, N]:
        # replace variable occurrences
        # for line in list(state.occurrences[fact].get(var, [])) if line in state.rules:
        for line in list(state.occurrences[fact].get(var, [])):
            if line in state.rules:
                rule = state.rules[line]
                if belief == fact:
                    # data agrees, OR rule satisfied, ditch whole rule
                    for key, val in rule.items():
                        occs = state.occurrences[val].get(key, set())
                        occs.discard(line)
                        if not occs:
                            # check occurrences opposite belief
                            if state.occurrences[-val].get(key, set()):
                                # other exists: pure literal clause
                                state.due_pure.add(key)
                            else:
                                # if both empty ditch both
                                state.occurrences[Y].pop(key, None)
                                state.occurrences[N].pop(key, None)
                    state.rules.pop(line, None)
                else:
                    # data opposite, ditch option from rule
                    rule.pop(var, None)
                    if not rule:
                        # empty clause: clash
                        return (N, state)
                    if len(rule) == 1:
                        # 1 left: unit clause
                        state.due_unit.add(line)
        state.occurrences[fact].pop(var, None)      # timing?
    state.due_pure.discard(var)
    return (Y, state)

def parse_dimacs_row(row):
    '''parse a line from a dimacs file into a dict, or None in case of a tautology'''
    dic = {}
    for term in row.split(' ')[:-1]:
        is_neg = term[0] == '-'
        key = int(term[1:]) if is_neg else int(term)
        val = N if is_neg else Y
        if key not in dic:
            dic[key] = val
        elif dic[key] != val:
            # different truth value known for this key, tautology detected
            return None
    return dic

def parse_dimacs(dimacs_file_contents):
    '''parse a dimacs file to rules (dict of dicts), cleaning out tautologies'''
    clause_dict = {}
    rows = list(filter(lambda s: s[0] not in ['c', 'p', 'd'], dimacs_file_contents))
    for (i, row) in enumerate(rows):
        clause = parse_dimacs_row(row)
        # skip tautologies
        if clause:
            clause_dict[i] = clause
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

def pick_guess_fact_random(_rules, occurrences):
    '''Picks an unassigned variable at random'''
    available_keys = list(occurrences[Y].keys())
    return random.choice(available_keys)

def pick_guess_fact_bohm(rules, occurrences, alpha=1, beta=2):
    '''Picks an unassigned variable based on the BOHM heuristic'''
    bohm = {}
    counts = {}
    available_keys = list(occurrences[Y].keys())
    max_clause_size = max([len(x) for x in list(rules.values())])
    for available_key in available_keys:
        bohm[available_key], counts[available_key] = {}, {}
        for clause_size in range(max_clause_size):
            counts[available_key][clause_size] = {}
            positive_count = len([1 for clause_index in occurrences[Y][available_key]
                                  if len(rules[clause_index]) == clause_size + 1])
            negative_count = len([1 for clause_index in occurrences[N][available_key]
                                  if len(rules[clause_index]) == clause_size + 1])
            right = beta * min(positive_count, negative_count)
            bohm[available_key][clause_size] = alpha * max(positive_count, negative_count) + right
            counts[available_key][clause_size][Y] = positive_count
            counts[available_key][clause_size][N] = negative_count
    for clause_size in range(max_clause_size):
        heuristics = [bohm[available_key][clause_size] for available_key in available_keys]
        if heuristics.count(max(heuristics)) > 1:
            continue
        else:
            max_key = available_keys[heuristics.index(max(heuristics))]
            if counts[max_key][clause_size][Y] >= counts[max_key][clause_size][N]:
                return max_key, Y
            return max_key, N

def simplify(state):
    '''apply pure / unit clause rules until stuck.
    returns (satisfiability, rules, facts).'''
    while state.due_pure or state.due_unit:

        # https://python.org/dev/peps/pep-0572/
        while True:
            var = state.due_pure.pop() if state.due_pure else None
            if not var:
                break

            # pure literal rule: regard occurrences as true if they all agree
            belief = Y if state.occurrences[Y].get(var, set()) else N
            if (Y if state.occurrences[N].get(var, set()) else N) != belief:
                (sat, state) = add_fact(state, var, belief)
                if sat == N:
                    return (sat, state)

        # https://python.org/dev/peps/pep-0572/
        while True:
            line = state.due_unit.pop() if state.due_unit else None
            if not line:
                break

            # unit clause rule: regard sole clauses as true
            if line in state.rules:
                rule = state.rules[line]
                if rule:
                    [(var, belief)] = list(rule.items())
                    (sat, state) = add_fact(state, var, belief)
                    if sat == N:
                        return (sat, state)

    sat = U if state.rules else Y
    return (sat, state)

def split(state_, facts_printer, fact_printer):
    '''guess a fact to proceed after simplify fails.'''
    state = pickle.loads(pickle.dumps(state_, -1))

    guess_fact = pick_guess_fact(state.rules)
    print_fact = fact_printer(guess_fact)
    guess_value = Y  # TODO: maybe also guess false?
    logging.info('guess     %d: %d', print_fact, guess_value)
    logging.debug(facts_printer(state.facts))
    (sat, state) = add_fact(state, guess_fact, guess_value)
    if sat != N:
        (sat, state) = simplify(state)
        if sat == U:
            (sat, state) = split(state, facts_printer, fact_printer)
    if sat == N:
        # clash detected, backtrack
        corrected = -guess_value  # opposite of guess
        (sat, state) = add_fact(state_, guess_fact, corrected)
        if sat == N:
            return (sat, state)
        # TODO: backtrack to assumption of clashing fact?
        logging.info('backtrack %d: %d', print_fact, corrected)
        logging.debug(facts_printer(state.facts))
        (sat, state) = simplify(state_)
        if sat == U:
            (sat, state) = split(state, facts_printer, fact_printer)
    return (sat, state)

def get_occurrences(rules, belief):
    '''get rule occurrences for a belief, e.g. { 123: set([3, 10]) }'''
    belief_occurrences = defaultdict(lambda: set())
    for line, ors in rules.items():
        for key, val in ors.items():
            if val == belief:
                # TODO: find alternative to this snippet that doesn't add 0.07s
                idx_set = belief_occurrences.get(key, set())
                idx_set.add(line)
                belief_occurrences[key] = idx_set
    return dict(belief_occurrences)

def solve_csp(rules, out_file, fact_printer=dict):
    '''solve a general CSP problem and write its solution to a file. returns satisfiability.'''
    start = time.time()

    try:
        logging.debug('initialization')
        state = State(rules)
        logging.debug(fact_printer(state.facts))

        logging.debug('simplify')
        (sat, state) = simplify(state)
        assert sat != N
        logging.debug(fact_printer(state.facts))

        logging.debug('split to answer')
        if sat == U:
            (sat, state) = split(state, fact_printer, EYE)
        assert sat != N
    except AssertionError:
        pass
    logging.warning('took %f seconds', time.time() - start)
    logging.debug('final solution')
    logging.warning(fact_printer(state.facts))

    # output DIMACS file 'filename.out' with truth assignments
    write_dimacs(out_file, state.facts)
    return sat == Y
