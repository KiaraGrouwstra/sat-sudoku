'''test Davis-Putnam functions'''
import os
import tempfile
from dp import parse_dimacs, read_file, write_dimacs, pick_guess_fact, simplify_initial, \
               simplify, split, Y, N, U, EYE, get_occurrences, State, parse_dimacs_row

def test_parse_dimacs_row():
    '''test'''
    assert parse_dimacs_row('123 -456 0') == {123:Y, 456:N}
    assert parse_dimacs_row('123 -123 0') == None

def test_parse_dimacs():
    '''test'''
    assert parse_dimacs(['123 -456 0']) == {0:{123:Y, 456:N}}
    assert parse_dimacs(['123 -123 0']) == {}

# def test_read_file():
#     '''test'''
#     assert len(read_file(example_fn)) == 18

def test_write_dimacs():
    '''test'''
    tmp_file = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))
    write_dimacs(tmp_file, {123: Y})
    assert read_file(tmp_file) == {0: {123: Y}}

def test_pick_guess_fact():
    '''test'''
    assert pick_guess_fact({0:{123:1}}) == 123

def test_simplify_initial():
    '''test'''
    rules = {0:{111:Y}}
    facts = {111:Y, 222:U}
    state = State(rules, facts)
    assert simplify_initial(state)[1].rules == {}

def test_simplify():
    '''test'''
    rules = {0:{0:Y, 1:Y}}
    facts = {0:Y, 1:U}
    state = State(rules, facts)
    assert simplify(state)[0] == Y
    rules = {0:{0:N, 1:N}}
    facts = {0:Y, 1:Y}
    state = State(rules, facts)
    assert simplify(state)[0] == N
    rules = {0:{0:Y, 1:Y}}
    facts = {0:U, 1:U}
    state = State(rules, facts)
    assert simplify(state)[0] == U

def test_split():
    '''test'''
    rules = {0:{0:N, 1:N}}
    facts = {0:U, 1:U}
    state = State(rules, facts)
    assert split(state, EYE, EYE)[0] == Y

def test_get_occurrences():
    '''test'''
    assert get_occurrences({123: {0:Y, 1:N}}, Y) == {0:set([123])}
