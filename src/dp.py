'''generic functions related to Davis-Putnam not specific to sudoku'''
import copy
import time
import logging
from collections import defaultdict
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

    def __init__(self, rules, facts):
        self.rules = rules
        self.facts = facts
        self.occurrences = {belief: get_occurrences(rules, belief) for belief in [Y, N]}

# Necessary Helper Functions

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
    for i in range(len(rows)):
        clause = parse_dimacs_row(rows[i])
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

# TODO: dedupe logic with simplify
def simplify_initial(state):
    '''do a one-time clean-up of pure-literal clauses.'''
    temp_rules = copy.copy(state.rules)
    for (rules_idx, ors) in temp_rules.items():

        res = {}
        for (key, belief) in ors.items():
            # clean out unit clauses
            # TODO: properly implement pure literal removal
            # if only one option...
            if len(ors) == 1:
                [(key, belief)] = list(ors.items())
                if state.facts.get(key, U) == -belief:    # opposite beliefs
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
        logging.debug(f'{len(state.rules)} rules left')
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
                            if state.facts.get(key, U) == -belief:    # opposite beliefs
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
    logging.info(f'guess     {print_fact}: {guess_value}')
    logging.debug(facts_printer(state.facts))
    (sat, state) = simplify(state)

    if sat == U:
        (sat, state) = split(state, facts_printer, fact_printer)
    if sat == N:
        # clash detected, backtrack
        corrected = -guess_value  # opposite of guess
        state_.facts[guess_fact] = corrected
        # TODO: backtrack to assumption of clashing fact?
        logging.info(f'backtrack {print_fact}: {corrected}')
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

    logging.debug('initialization')
    # initialize facts as U
    facts = {}
    logging.debug(fact_printer(facts))
    state = State(rules, facts)

    logging.debug('simplify init')
    (sat, state) = simplify_initial(state)
    # assert sat != N
    if sat == N:
        return False
    logging.debug(fact_printer(state.facts))

    logging.debug('simplify')
    (sat, state) = simplify(state)
    # assert sat != N
    if sat == N:
        return False
    logging.debug(fact_printer(state.facts))

    logging.debug('split to answer')
    if sat == U:
        (sat, state) = split(state, fact_printer, EYE)
    # assert sat != N
    if sat == N:
        return False

    logging.warning(f'took {time.time() - start} seconds')
    logging.debug('final solution')
    logging.warning(fact_printer(state.facts))

    # output DIMACS file 'filename.out' with truth assignments, TODO: empty if inconsistent.
    write_dimacs(out_file, state.facts)

    return sat == Y
