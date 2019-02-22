# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# run locally
python src/solve-sat.py -p1 -S1 ./data/sudoku-example-full.txt
# or by docker
docker run -v $PWD:/app python:3.7-alpine python /app/src/solve-sat.py -p1 -S1 /app/data/sudoku-example-full.txt
# TODO: intended usage
SAT -S2 sudoku_nr_10
```
