'''functions to pick a fact to guess.'''
import random
from collections import defaultdict
import numpy as np
from dp import Y, N

def guess_random(_rules, occurrences):
    '''Picks an unassigned variable at random.
    presume pure literals are pruned, so keys in Y and N are identical.'''
    keys = list(occurrences[Y].keys())
    return (random.choice(keys), Y)

def guess_dlcs(rules, _occurrences):
    '''Dynamic Largest Combined Sum heuristic.
    presume all known facts are pruned, so only tally facts in rules.'''
    relevances = defaultdict(lambda: 0, {})
    for ors in rules.values():
        for key in ors:
            relevances[key] += 1
    return (max(relevances), Y)

def guess_jw_ts(rules, occurrences):
    '''Picks decision variable based on the Jeroslow-Wang Two Sided Heuristic'''
    available_keys = list(occurrences[Y].keys())
    positive_counts = np.array([sum([2 ** -len(rules[clause_index])
                                     for clause_index in occurrences[Y][available_key]
                                     if rules.get(clause_index, N) != N])
                                for available_key in available_keys])
    negative_counts = np.array([sum([2 ** -len(rules[clause_index])
                                     for clause_index in occurrences[N][available_key]
                                     if rules.get(clause_index, N) != N])
                                for available_key in available_keys])
    jw_sum = positive_counts + negative_counts
    return (available_keys[np.argmax(jw_sum)], Y
            if positive_counts[np.argmax(jw_sum)] >= negative_counts[np.argmax(jw_sum)] else N)

def guess_bohm(rules, occurrences, alpha=1, beta=2):
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
