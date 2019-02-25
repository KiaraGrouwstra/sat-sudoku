'''a script to run the example sudokus to verify our algorithm'''
import os
import glob
import logging
from sat import monitor_runs, Algorithm

def main():
    fpaths = glob.glob(os.path.join(os.getcwd(), 'data', 'dimacs', '*', '*.in'))
    # logging.warning('solving sudokus')
    alg = Algorithm.RANDOM
    # logging.warning(alg.name)
    # df = 
    monitor_runs(fpaths, alg=alg, loglvl=logging.ERROR)
    # solved = df['solved'].tolist()
    # logging.error(f"Solved: {solved.count(True)}, Unsolved: {solved.count(False)}")

if __name__ == "__main__":
    main()
