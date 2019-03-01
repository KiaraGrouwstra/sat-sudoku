'''test'''
from dp import Y, N
from heuristics import guess_random, guess_dlcs, guess_dscs, guess_dlis, guess_jw_1s, \
                       guess_jw_2s, guess_mom, guess_fom, guess_bohm_, \
                       guess_bohm

rules = {0:{123:Y,456:Y,789:Y},1:{123:N,456:N},2:{456:N,789:N}}
occurrences = {Y:{123:{0},456:{0},789:{0}}, N:{123:{1},456:{1,2},789:{2}}}

def test_guess_random():
    '''test'''
    fact, belief = guess_random(rules, occurrences)
    assert fact in {123,456,789}

def test_guess_dlcs():
    '''test'''
    assert guess_dlcs(rules, occurrences) == (789, N)

def test_guess_dscs():
    '''test'''
    assert guess_dscs(rules, occurrences) == (123, N)

def test_guess_dlis():
    '''test'''
    assert guess_dlis(rules, occurrences) == (789, Y)

def test_guess_jw_1s():
    '''test'''
    assert guess_jw_1s(rules, occurrences) == (789, N)

def test_guess_jw_2s():
    '''test'''
    assert guess_jw_2s(rules, occurrences) == (789, N)

# def test_guess_jw_ts():
#     '''test'''
#     assert guess_jw_ts(rules, occurrences) == (456, N)

def test_guess_mom():
    '''test'''
    assert guess_mom(rules, occurrences) == (789, N)

def test_guess_fom():
    '''test'''
    assert guess_fom(rules, occurrences) == (123, N)

def test_guess_bohm_():
    '''test'''
    assert guess_bohm_(rules, occurrences) == (456, N)

def test_guess_bohm():
    '''test'''
    assert guess_bohm(rules, occurrences) == (456, N)
