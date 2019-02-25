'''test'''
from dp import Y, N
from heuristics import pick_guess_fact_random, pick_guess_fact_dlcs, \
                                pick_guess_fact_jw_ts, pick_guess_fact_bohm

def test_pick_guess_fact_random():
    '''test'''
    assert pick_guess_fact_random({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_pick_guess_fact_dlcs():
    '''test'''
    assert pick_guess_fact_dlcs({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_pick_guess_fact_jw_ts():
    '''test'''
    # assert pick_guess_fact_jw_ts({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_pick_guess_fact_bohm():
    '''test'''
    # assert pick_guess_fact_bohm({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)
