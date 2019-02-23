from dp import *

def test_parse_dimacs():
  assert parse_dimacs(['123 -456 0']) == {0:{123:Y, 456:N}}
  assert parse_dimacs(['123 -123 0']) == {}

# def test_read_file():
#   assert len(read_file(example_fn)) == 18

def test_write_dimacs():
  tmp_file = os.path.join(tempfile.gettempdir(), next(tempfile._get_candidate_names()))
  write_dimacs(tmp_file, {'123': Y})
  assert read_file(tmp_file) == {0: {123: 1}}

def test_pick_guess_fact():
  assert pick_guess_fact({0:{123:1}}, {}) == 123

def test_simplify_initial():
  assert simplify_initial({0:{111:1}}, {111:1, 222:0})[1] == {}

def test_simplify():
  assert simplify({0:{0:Y, 1:Y}}, {0:Y, 1:U })[0] == Y
  assert simplify({0:{0:N, 1:N}}, {0:Y, 1:Y })[0] == N
  assert simplify({0:{0:Y, 1:Y}}, {0:U, 1:U })[0] == U

def test_split():
  assert split({0:{0:N, 1:N}}, {0:U, 1:U}, eye, eye)[0] == Y
