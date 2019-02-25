#!/usr/bin/python

'''cli program'''
import argparse
import logging
from dp import read_file, solve_csp
from heuristics import pick_guess_fact_random, pick_guess_fact_dlcs, pick_guess_fact_jw_ts
from sudoku import sudoku_board

def main():
    '''take cli flags and solve SAT problem'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--strategy', dest='strategy', type=int, default=1,
                        help='1 for the basic DP and n = 2 or 3 for your two other strategies')
    parser.add_argument('-l', '--loglevel', dest='loglevel', type=int, default=1,
                        help='0 for debug, 1 for info (default), 2 for warn, 3 for error')
    parser.add_argument('-p', '--printer', default=False, action='store_true',
                        help='print solution as sudoku instead of dict')
    parser.add_argument('inputfiles', nargs='*', default=['./data/sudoku-example-full.txt'],
                        help='the input file is the concatenation of all required input clauses.')

    args = parser.parse_args()

    fact_printer = sudoku_board if args.printer == 1 else dict
    guess_fn = {
        1:pick_guess_fact_random,
        2:pick_guess_fact_dlcs,
        3:pick_guess_fact_jw_ts
    }.get(args.strategy, pick_guess_fact_random)

    lvl = args.loglevel
    loglvl = logging.DEBUG if lvl == 0 \
        else logging.WARN if lvl == 2 \
        else logging.ERROR if lvl == 3 \
        else logging.INFO
    logging.getLogger().setLevel(loglvl)

    for inputfile in args.inputfiles:
        logging.debug(inputfile)
        clauses = read_file(inputfile)
        logging.debug(clauses)
        out_file = inputfile + '.out'
        logging.error(solve_csp(clauses, out_file, guess_fn, fact_printer))

if __name__ == '__main__':
    main()
