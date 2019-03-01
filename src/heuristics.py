'''functions to pick a fact to guess.'''
import random
from collections import defaultdict
# import numpy as np
from dp import Y, N

def guess_random(_rules, occurrences):
    '''Picks an unassigned variable at random.
    presume pure literals are pruned, so keys in Y and N are identical.'''
    keys = list(occurrences[Y].keys())
    fact = random.choice(keys)
    belief = Y if random.getrandbits(1) else N
    return (fact, belief)

# https://stackoverflow.com/questions/16560840/python-merge-dictionaries-with-custom-merge-function
def merge(A, B, f):
    # keys either in A or B, but not both
    merged = {k: A.get(k, B.get(k)) for k in A.keys() ^ B.keys()}
    # Update with `f()` applied to the intersection
    merged.update({k: f(A[k], B[k]) for k in A.keys() & B.keys()})
    return merged

def guess_dlcs(rules, occurrences):
    '''
    Dynamic Largest Combined Sum heuristic.
    presume all known facts are pruned, so only tally facts in rules.
    Pick v with largest CP(v)+CN(v) (= most frequent v).
    If CP(v)>CN(v) then v=1 else v=0.
    '''
    # score: number of occurrences
    # print(list(occurrences[Y].values())[0])
    print(occurrences[Y])
    score = { belief: { fact: len(idxs) for fact, idxs in occs.items() } for belief, occs in occurrences.items() }
    # pick: 2-sided
    merged_score = merge(score[Y], score[N], lambda a, b: a + b)
    fact = max(merged_score)
    belief = Y if score[Y][fact] > score[N][fact] else N
    return (fact, belief)

def guess_dscs(rules, occurrences):
    '''Dynamic Smallest Combined Sum'''
    # score: number of occurrences
    score = { belief: { fact: len(idxs) for fact, idxs in occs.items() } for belief, occs in occurrences.items() }
    # pick: 2-sided, min
    merged_score = merge(score[Y], score[N], lambda a, b: a + b)
    fact = min(merged_score)
    belief = Y if score[Y][fact] > score[N][fact] else N
    return (fact, belief)

def guess_dlis(rules, occurrences):
    '''
    Dynamic Largest Individual Sum heuristic.
    Pick v with largest CP(v) or largest CN(v), breaking ties in favor of CP.
    If CP(v)>CN(v) then v=1 else v=0.
    '''
    # score: number of occurrences
    score = { belief: { fact: len(idxs) for fact, idxs in occs.items() } for belief, occs in occurrences.items() }
    # pick: 1-sided
    fact_pos = max(score[Y])
    fact_neg = max(score[N])
    is_pos = score[Y][fact_pos] >= score[N][fact_neg]
    fact = fact_pos if is_pos else fact_neg
    belief = Y if is_pos else N
    return (fact, belief)

def guess_jw_1s(rules, occurrences):
    '''Jeroslow-Wang One Sided'''
    # score: prioritize small clauses
    score = { belief: { fact: sum([2 ** -len(rules[idx]) for idx in idxs]) for fact, idxs in occs.items() } for belief, occs in occurrences.items() }
    # pick: 1-sided
    fact_pos = max(score[Y])
    fact_neg = max(score[N])
    is_pos = score[Y][fact_pos] >= score[N][fact_neg]
    fact = fact_pos if is_pos else fact_neg
    belief = Y if is_pos else N
    return (fact, belief)

def guess_jw_2s(rules, occurrences):
    '''Jeroslow-Wang One Sided'''
    # score: prioritize small clauses
    score = { belief: { fact: sum([2 ** -len(rules[idx]) for idx in idxs]) for fact, idxs in occs.items() } for belief, occs in occurrences.items() }
    # pick: 2-sided
    merged_score = merge(score[Y], score[N], lambda a, b: a + b)
    fact = max(merged_score)
    belief = Y if score[Y][fact] > score[N][fact] else N
    return (fact, belief)

# def guess_jw_ts(rules, occurrences):
#     '''Picks decision variable based on the Jeroslow-Wang Two Sided Heuristic'''
#     available_keys = list(occurrences[Y].keys())
#     positive_counts = np.array([sum([2 ** -len(rules[clause_index])
#                                      for clause_index in occurrences[Y][available_key]
#                                      if rules.get(clause_index, N) != N])
#                                 for available_key in available_keys])
#     negative_counts = np.array([sum([2 ** -len(rules[clause_index])
#                                      for clause_index in occurrences[N][available_key]
#                                      if rules.get(clause_index, N) != N])
#                                 for available_key in available_keys])
#     jw_sum = positive_counts + negative_counts
#     return (available_keys[np.argmax(jw_sum)], Y
#             if positive_counts[np.argmax(jw_sum)] >= negative_counts[np.argmax(jw_sum)] else N)

def guess_mom(rules, occurrences, k=1):
    '''Maximum Occurrences in Clauses of Minimum Size'''
    # score: prioritize small clauses
    rule_lens = {idx: len(dic) for idx, dic in rules.items()}
    min_rule_len = min(rule_lens.values())
    min_rules = [rules[k] for k, v in rule_lens.items() if v == min_rule_len]

    # number of occurrences of I in the smallest non-satisfied clauses
    facts = occurrences[Y].keys()  # assume same keys in Y and N
    f = {belief: {k:0 for k in facts} for belief in [Y, N]}
    for ors in min_rules:
        for fact, belief in ors.items():
            f[belief][fact] += 1

    merged_score = {fact: (f[Y][fact] + f[N][fact]) * 2**k + f[Y][fact] * f[N][fact]
                    for fact in facts}

    # pick: 2-sided, w/ above merged_score
    fact = max(merged_score)
    belief = Y if f[Y][fact] > f[N][fact] else N
    return (fact, belief)

def guess_fom(rules, occurrences):
    '''First Occurrence in Clauses of Minimum Size'''
    # score: prioritize small clauses
    rule_lens = {idx: len(dic) for idx, dic in rules.items()}
    min_rule_idx = min(rule_lens)
    min_rule = rules[min_rule_idx]
    fact = list(min_rule.keys())[0]
    # belief: opposite of that in short rule
    belief = -min_rule[fact]
    return (fact, belief)

def guess_bohm_(rules, occurrences, alpha=1, beta=2):
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

def guess_bohm(rules, occurrences, alpha=1, beta=2):
    '''Bohm'''
    # score: gives preference to variables that are satisfying small clauses or that are reducing the size of already small clauses
    rule_lens = {idx: len(dic) for idx, dic in rules.items()}
    facts = occurrences[Y].keys()  # assume same keys in Y and N
    min_rule_len = min(rule_lens.values())
    max_rule_len = max(rule_lens.values())
    for rule_len in range(min_rule_len, max_rule_len+1):
        if len(facts) == 1:
            fact = facts[0]
            break
        len_rules = [rules[k] for k, v in rule_lens.items() if v == rule_len]

        # number of occurrences of I in the smallest non-satisfied clauses
        f = {belief: defaultdict(lambda: 0, {}) for belief in [Y, N]}
        for ors in len_rules:
            for fact, belief in ors.items():
                f[belief][fact] += 1

        merged_score = {fact: alpha * max(f[Y][fact], f[N][fact]) + beta * min(f[Y][fact], f[N][fact])
                        for fact in facts}
        max_score = max(merged_score.values())
        facts = [fact for fact, score in merged_score.items() if score == max_score]

    belief = Y if f[Y][fact] > f[N][fact] else N
    return (fact, belief)
