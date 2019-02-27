'''a script to run the example sudokus to verify our algorithm'''
import os
import glob
import logging
from sat import monitor_runs, Algorithm

def main():
    fpaths = glob.glob(os.path.join(os.getcwd(), 'data', 'dimacs', '*', '*.in'))
    for alg in Algorithm:
        logging.error(alg.name)
        monitor_runs(fpaths, alg=alg, loglvl=logging.ERROR, fancy_beliefs=True)

if __name__ == "__main__":
    main()
