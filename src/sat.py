#!/usr/bin/python

'''cli program'''
import argparse
from dp import read_file, solve_csp
from sudoku import sudoku_board

def main():
    '''take cli flags and solve SAT problem'''
    parser = argparse.ArgumentParser()
    parser.add_argument("-S", "--strategy", dest="strategy", type=int, default=1,
                        help="1 for the basic DP and n=2 or 3 for your two other strategies")
    parser.add_argument("-p", "--printer", dest="printer", type=int, default=0,
                        help="1 for sudoku printer, otherwise dict")
    parser.add_argument('inputfiles', nargs='*', default=['./data/sudoku-example-full.txt'],
                        help='the input file is the concatenation of all required input clauses.')
    args = parser.parse_args()
    assert args.strategy == 1  # TODO: implement strategy cli handling
    fact_printer = sudoku_board if args.printer == 1 else dict

    for inputfile in args.inputfiles:
        clauses = read_file(inputfile)
        # print(clauses)
        out_file = inputfile + '.out'
        print(solve_csp(clauses, out_file, fact_printer))

if __name__ == "__main__":
    main()
