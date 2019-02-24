# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# running locally

# as a command (*nix environment)
src/SAT -S1 -p1 ./data/sudoku-example-full.txt
# as a Python script (cross-platform)
python src/SAT.py -p1 -S1 ./data/sudoku-example-full.txt

# running by docker

# build docker image
docker build -t sat .
# test image on sample file, using strategy 1, printer 1 (sudoku board)
docker run sat -S1 -p1
# run on local file on our Desktop, mounting to /data, and passing it the file
docker run -v ~/Desktop:/data sat -S1 -p1 /data/sudoku-example-full.txt

# dev

# install python deps thru conda
conda install pylint pytest
# run unit tests (also happens when building Docker image)
pytest
```
