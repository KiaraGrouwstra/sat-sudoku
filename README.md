# sat-sudoku
a SAT solver using sudokus

### usage
```bash
# run: local

# as a command (*nix environment)
./SAT -S1 -p -l2 ./data/sudoku-example-full.txt
# as a Python script (cross-platform)
python src/sat.py --help
# test image on sample file, using -p to print solution as a sudoku board, strategy 2, log level info
python src/sat.py -p -l2 -S2 ./data/sudoku-example-full.txt

# run: docker

# navigate to src directory
cd src
# build docker image, use backslashes on Windows
docker build -t sat .
# test script thru docker
docker run sat --help
# run on local file on our Desktop, mounting to /data, and passing it the file
docker run -v ~/Desktop:/data sat -S1 -p /data/sudoku-example-full.txt

# dev: local

# install python deps thru conda
conda install pylint pytest numpy
# run unit tests (also happens when building Docker image)
pytest
pylint ./src
# dev: docker

# docker split due to big deps
docker build -t sudoku-base -f ./docker/base/Dockerfile .
docker build -t sat -f ./docker/top/Dockerfile .
```
