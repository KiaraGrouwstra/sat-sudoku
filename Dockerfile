# Use an official Python runtime as a parent image
FROM python:3.7-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pylint .
RUN pytest

# Run script when the container launches
ENTRYPOINT ["python", "./src/SAT.py"]
