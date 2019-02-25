# Use an official Python runtime as a parent image
FROM sudoku-base

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN . activate base
RUN pylint ./src || true
RUN pytest

# Run script when the container launches
ENTRYPOINT ["python", "./src/sat.py"]
