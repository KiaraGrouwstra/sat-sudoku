# Use an official Python runtime as a parent image
FROM frolvlad/alpine-miniconda3

# Install any needed packages
RUN . activate base
RUN conda install pylint pytest numpy pandas seaborn
