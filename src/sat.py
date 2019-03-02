#!/usr/bin/python

'''cli program'''
import os
import argparse
import logging
from enum import Enum
from dp import read_file, solve_csp
from heuristics import guess_random, guess_dlcs, guess_dscs, guess_dlis, guess_jw_1s, \
                       guess_jw_2s, guess_mom, guess_fom, guess_bohm_, \
                       guess_bohm
from sudoku import sudoku_board

class Algorithm(Enum):
    RANDOM = 1
    DLCS = 2
    # DSCS = 3
    DLIS = 4
    JW_1S = 5
    JW_2S = 6
    # JW_TS = 7
    MOM = 8
    # FOM = 9
    # BOHM_ = 10
    # BOHM = 11

def monitor_runs(inputfiles, alg, fact_printer=dict, loglvl=logging.INFO,
                 # =Algorithm.RANDOM
                 fancy_beliefs=False,
                 output_file=os.path.join(os.getcwd(), 'data', 'metrics.csv')):
    '''run on some files and log results to csv'''
    logging.getLogger().setLevel(loglvl)

    guess_fn = {
        Algorithm.RANDOM: guess_random,
        Algorithm.DLCS: guess_dlcs,
        # Algorithm.DSCS: guess_dscs,
        Algorithm.DLIS: guess_dlis,
        Algorithm.JW_1S: guess_jw_1s,
        Algorithm.JW_2S: guess_jw_2s,
        # Algorithm.JW_TS: guess_jw_ts,
        Algorithm.MOM: guess_mom,
        # Algorithm.FOM: guess_fom,
        # Algorithm.BOHM_: guess_bohm_,
        # Algorithm.BOHM: guess_bohm,
    }[alg]

    res = []
    for inputfile in inputfiles:
        logging.debug(inputfile)
        clauses = read_file(inputfile)
        givens = len(list(filter(lambda x: len(x) == 1, clauses.values())))
        logging.debug(clauses)
        out_file = inputfile + '.out'
        (solved, state, secs, splits, backtracks, unit_applied, pure_applied) = solve_csp(clauses, out_file, guess_fn, fact_printer, fancy_beliefs)
        logging.warning(inputfile)
        logging.warning('%s, %f secs, %d splits, %d backtracks', solved, secs, splits, backtracks)
        logging.info(fact_printer(state.facts))
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
    return res

# https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
def str2bool(v):
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0', ''):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def main():
    '''take cli flags and solve SAT problem'''
    parser = argparse.ArgumentParser()
    parser.add_argument('-S', '--strategy', dest='strategy', type=int, default=1,
                        help='1 for the basic DP and n = 2 or 3 for your two other strategies')
    parser.add_argument('-l', '--loglevel', dest='loglevel', type=int, default=2,
                        help='0 for debug, 1 for info (default), 2 for warn, 3 for error')
    parser.add_argument('-p', '--printer', type=str2bool, nargs='?', default=False,
                        help='print solution as sudoku instead of dict')
    parser.add_argument('inputfiles', nargs='*', default=[os.path.join(os.getcwd(), 'data', 'dimacs', 'sudoku-example-full.txt')],
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
