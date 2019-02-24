'''generic functions related to Davis-Putnam not specific to sudoku'''
import copy
import time
from collections import defaultdict

# constants

U = 0
Y = 1
N = -1
EYE = lambda x: x

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
    '''pick a fact to guess. presume all known facts are pruned from rules
    (by simplify_initial), so only tally facts in rules.'''
    relevances = defaultdict(lambda: 0, {})
    for ors in rules.values():
        for key in ors:
            relevances[key] += 1
    return max(relevances)

# TODO: dedupe logic with simplify
def simplify_initial(rules, facts):
    '''do a one-time clean-up of tautologies and pure-literal clauses.'''
    temp_rules = copy.copy(rules)
    for (rules_idx, ors) in temp_rules.items():

        # tautology: p or not p is redundant
        # group beliefs by key
        res = {}
        for (key, belief) in ors.items():
            res.setdefault(key, []).append(belief)
            # check if any key has multiple (= complementing) beliefs
            if any(map(lambda arr: len(set(arr)) > 1, res.values())):
                # ditch fact
                # TODO: switch to linked list for constant-time deletions
                # TODO: or instead just create new list for the whole pass
                del rules[rules_idx]
                continue

            # clean out pure literals
            # if only one option...
            if len(ors) == 1:
                [(key, belief)] = list(ors.items())
                if facts[key] == -belief:  # opposite beliefs
                    # clash detected, report it
                    return (N, [], [])
                # consider it fact
                facts[key] = belief
                # we've exhausted the info in this rule, so get rid of it
                del rules[rules_idx]
                continue

    sat = U if len(rules) > 0 else Y
    return (sat, rules, facts)

def simplify(rules, facts):
    '''simplify out unit clauses until we get stuck.
        returns (satisfiability, rules, facts).'''
    prev_left = 0
    rules_left = len(rules)

    while rules_left != prev_left:
        # print(f'{len(rules)} rules left')
        temp_rules = copy.copy(rules)
        for (outer_key, ors) in temp_rules.items():
            temp_clause = copy.copy(ors)
            for (inner_key, belief) in temp_clause.items():
                # TODO: parallelize lookups with linalg
                fact = facts[inner_key]
                if fact != U:  # if we know something about this fact...
                    if belief == fact:
                        # data agrees, OR rule satisfied, ditch whole rule
                        del rules[outer_key]
                        break
                    else:
                        # data clashes, ditch option from rule
                        del ors[inner_key]
                        # del rules[rules_idx][ors_idx]
                        # if only one option remains...
                        if len(ors) == 1:
                            [(key, belief)] = list(ors.items())
                            if facts[key] == -belief:  # opposite beliefs
                                # clash detected, report it
                                return (N, [], [])
                            # consider it fact
                            facts[key] = belief
                            # we've exhausted the info in this rule, so get rid of it
                            del rules[outer_key]
                            break
                        continue
                # else:  # no data available, nothing to do here
        prev_left = rules_left
        rules_left = len(rules)
    sat = U if rules_left else Y
    return (sat, rules, facts)

def split(rules_, facts_, facts_printer, fact_printer):
    '''guess a fact to proceed after simplify fails.'''
    rules = copy.deepcopy(rules_)
    facts = copy.deepcopy(facts_)

    guess_fact = pick_guess_fact(rules)
    # print_fact = fact_printer(guess_fact)
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

def solve_csp(rules, out_file, fact_printer=dict):
    '''solve a general CSP problem and write its solution to a file. returns satisfiability.'''
    start = time.time()

    # print('initialization')
    facts = defaultdict(lambda: U, {})  # initialize facts as U
    # print(fact_printer(facts))

    # print('simplify init')
    (sat, rules, facts) = simplify_initial(rules, facts)
    # assert sat != N
    if sat == N:
        return False
    # print(fact_printer(facts))

    # print('simplify')
    (sat, rules, facts) = simplify(rules, facts)
    # assert sat != N
    if sat == N:
        return False
    # print(fact_printer(facts))

    # print('split to answer')
    if sat == U:
        (sat, rules, facts) = split(rules, facts, fact_printer, EYE)
    # assert sat != N
    if sat == N:
        return False

    #print(f'took {time.time() - start} seconds')
    # print('final solution')
    #print(fact_printer(facts))

    # output DIMACS file 'filename.out' with truth assignments, TODO: empty if inconsistent.
    write_dimacs(out_file, facts)

    return sat == Y
