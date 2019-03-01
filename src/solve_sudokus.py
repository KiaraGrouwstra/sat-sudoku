'''a script to run the example sudokus to verify our algorithm'''
import os
import glob
import logging
import pandas as pd
from sat import monitor_runs, Algorithm

def main():
    # fpaths = glob.glob(os.path.join(os.getcwd(), 'data', 'dimacs', 'sudoku', '*', '*.in'))
    # fpaths = glob.glob(os.path.join(os.getcwd(), 'data', 'dimacs', 'sudoku', 'janne', '*.in'))
    fpaths = glob.glob(os.path.join(os.getcwd(), 'data', 'dimacs', 'other', '*', '*.txt'))
    for belief in [
        # True,
        False,
    ]:
        for alg in Algorithm:
            logging.error(alg.name)
            res = monitor_runs(fpaths, alg=alg, loglvl=logging.ERROR, fancy_beliefs=belief)
            df = pd.DataFrame(res)
            if os.path.isfile(output_file):
                df.to_csv(path_or_buf=output_file, header=False, mode='a')
            else:
                df.to_csv(path_or_buf=output_file, header=True, mode='w')

if __name__ == "__main__":
    main()
