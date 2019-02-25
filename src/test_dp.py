'''test Davis-Putnam functions'''
import os
import tempfile
from dp import parse_dimacs, read_file, write_dimacs, simplify, split, \
               Y, N, U, EYE, get_occurrences, State, parse_dimacs_row, add_fact
from heuristics import guess_random

def test_state():
    '''test'''
    state = State({0:{111:Y}, 1:{111:N, 222:Y}})
    assert state.rules == {0:{111:Y}, 1:{111:N, 222:Y}}
    assert state.facts == {}
    assert state.occurrences == {1: {111: {0}, 222: {1}}, -1: {111: {1}}}
    assert state.due_pure == {222}
    assert state.due_unit == {0}

def test_add_fact():
    '''test'''
    state = State({0:{111:Y}, 1:{111:N, 222:Y}})
    (sat, state) = add_fact(state, 111, Y)
    assert sat == Y
    assert state.rules == {1: {222: Y}}
    assert state.facts == {111: Y}
    assert state.occurrences == {Y: {222: {1}}, N: {}}
    assert state.due_pure == {222}
    assert state.due_unit == {0, 1}

def test_parse_dimacs_row():
    '''test'''
    assert parse_dimacs_row('123 -456 0') == {123:Y, 456:N}
    assert parse_dimacs_row('123 -123 0') is None

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

def test_simplify():
    '''test'''
    rules = {0:{0:Y, 1:Y}, 1:{0:Y}}
    state = State(rules)
    assert simplify(state)[0] == Y
    rules = {0:{0:N, 1:N}, 1:{0:Y}, 2:{1:Y}}
    state = State(rules)
    assert simplify(state)[0] == N
    rules = {0:{0:Y, 1:Y}, 1:{0:N, 1:N}}
    state = State(rules)
    assert simplify(state)[0] == U

def test_split():
    '''test'''
    state = State({0:{0:Y, 1:Y}, 1:{0:N, 1:N}})
    (sat, state) = simplify(state)
    (sat, state) = split(state, EYE, EYE, guess_random)
    assert sat == Y

def test_get_occurrences():
    '''test'''
    assert get_occurrences({123: {0:Y, 1:N}}, Y) == {0:set([123])}
