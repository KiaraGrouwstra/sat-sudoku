# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# running locally

# as a command (*nix environment)
./SAT -S1 -p -l2 ./data/sudoku-example-full.txt
# as a Python script (cross-platform)
python src/sat.py --help
python src/sat.py -p -l2 -S2 ./data/sudoku-example-full.txt

# running by docker

# build docker image
docker build -t sat .
# test image on sample file, using strategy 1, printer 1 (sudoku board)
docker run sat -S1 -p
# run on local file on our Desktop, mounting to /data, and passing it the file
docker run -v ~/Desktop:/data sat -S1 -p /data/sudoku-example-full.txt

# dev

# install python deps thru conda
conda install pylint pytest numpy
# run unit tests (also happens when building Docker image)
pytest
```
