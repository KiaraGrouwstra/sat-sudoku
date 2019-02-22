# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# run locally
src/SAT -p1 -S1 ./data/sudoku-example-full.txt
# or by docker
docker run -v $PWD:/app python:3.7-alpine python /app/src/SAT.py -p1 -S1 /app/data/sudoku-example-full.txt
```
