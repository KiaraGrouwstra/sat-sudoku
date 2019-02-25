#!/usr/bin/python

'''cli program'''
import argparse
import logging
from enum import Enum
import pandas as pd
from dp import read_file, solve_csp
from heuristics import guess_random, guess_dlcs, guess_jw_ts, guess_bohm
from sudoku import sudoku_board

class Algorithm(Enum):
    RANDOM = 1
    DLCS = 2
    JW_TS = 3
    BOHM = 4

def monitor_runs(inputfiles, alg=Algorithm.RANDOM, fact_printer=dict, loglvl=logging.INFO,
                 fancy_beliefs=False, output_file='./data/metrics.csv'):
    '''run on some files and log results to csv'''
    logging.getLogger().setLevel(loglvl)

    guess_fn = {
        Algorithm.RANDOM: guess_random,
        Algorithm.DLCS: guess_dlcs,
        Algorithm.JW_TS: guess_jw_ts,
        Algorithm.BOHM: guess_bohm,
    }[alg]

    res = []
    for inputfile in inputfiles:
        logging.debug(inputfile)
        clauses = read_file(inputfile)
        givens = len(list(filter(lambda x: len(x) == 1, clauses.values())))
        logging.debug(clauses)
        out_file = inputfile + '.out'
        (solved, state, secs, splits, backtracks, unit_applied, pure_applied) = solve_csp(clauses, out_file, guess_fn, fact_printer)
        logging.error('%s, took %d splits, %d backtracks, %f seconds, %d unit applied, %d pure applied', solved, splits, backtracks, secs, unit_applied, pure_applied)
        logging.warning(fact_printer(state.facts))
        res.append({
            'inputfile': inputfile,
            'solved': solved,
            # 'state': state,
            'assigned': len(state.facts),
            'secs': round(secs, 3),
            'splits': splits,
            'backtracks': backtracks,
            'unit_applied': unit_applied,
            'pure_applied': pure_applied,
            'alg': alg.name,
            'fancy_beliefs': fancy_beliefs,
            'givens': givens,
            # '': ,
        })
    df = pd.DataFrame(res)
    df.to_csv(path_or_buf=output_file)

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
    parser.add_argument('-b', '--beliefs', default=False, action='store_true', help='fancy beliefs for our experiment')

    args = parser.parse_args()

    fact_printer = sudoku_board if args.printer == 1 else dict
    fancy_beliefs = args.beliefs
    inputfiles = args.inputfiles
    alg = Algorithm(args.strategy)

    loglvl = {
        0:logging.DEBUG,
        1:logging.INFO,
        2:logging.WARN,
        3:logging.ERROR,
    }.get(args.loglevel, logging.INFO)
    monitor_runs(inputfiles, alg, fact_printer, loglvl, fancy_beliefs)

if __name__ == '__main__':
    main()
