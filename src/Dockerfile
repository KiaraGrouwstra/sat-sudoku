# Use an Alpine Conda image
FROM frolvlad/alpine-miniconda3

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/src

# Run script when the container launches
ENTRYPOINT ["python", "./src/sat.py"]
