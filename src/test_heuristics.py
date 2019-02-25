'''test'''
from dp import Y, N
from heuristics import guess_random, guess_dlcs, \
                                guess_jw_ts, guess_bohm

def test_guess_random():
    '''test'''
    assert guess_random({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_guess_dlcs():
    '''test'''
    assert guess_dlcs({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_guess_jw_ts():
    '''test'''
    # assert guess_jw_ts({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)

def test_guess_bohm():
    '''test'''
    # assert guess_bohm({0:{123:1}}, {N:{}, Y:{123:0}}) == (123, Y)
