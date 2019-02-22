# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# run locally
python src/solve-sudoku.py
# or by docker
docker run -v $PWD:/app python:3.7-alpine python /app/src/solve-sudoku.py
# TODO: intended usage
SAT -S2 sudoku_nr_10
# where SAT is the (compulsory) name of your program, n=1 for the basic DP and n=2 or 3 for your two other strategies, and the input file is the concatenation of all required input clauses (in your case: sudoku rules + given puzzle)
```
