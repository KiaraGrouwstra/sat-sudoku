# Use an official Python runtime as a parent image
FROM frolvlad/alpine-miniconda3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN . activate base
RUN conda install pylint pytest numpy seaborn
RUN pylint ./src || true
RUN pytest

# Run script when the container launches
ENTRYPOINT ["python", "./src/sat.py"]
