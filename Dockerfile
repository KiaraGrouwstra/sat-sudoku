# Use an official Python runtime as a parent image
FROM python:3.7-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Run script when the container launches
ENTRYPOINT ["python", "./src/SAT.py"]
