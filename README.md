# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# run locally as a command (*nix environment)
src/SAT -S1 -p1 ./data/sudoku-example-full.txt
# run explicitly as a Python script (cross-platform)
python src/SAT.py -p1 -S1 ./data/sudoku-example-full.txt
# or by docker...
# build docker image
docker build -t sat .
# test image on sample file, using strategy 1, printer 1 (sudoku board)
docker run sat -S1 -p1
# run on local file on our Desktop, mounting to /data, and passing it the file
docker run -v ~/Desktop:/data sat -S1 -p1 /data/sudoku-example-full.txt
```
