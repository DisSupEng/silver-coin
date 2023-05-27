# Use python 3.10
FROM python:3.10
# Update and install packages
RUN apt update && apt upgrade -y

# Copy the source files
RUN mkdir /src
COPY . /src
WORKDIR /src

# Update pip
RUN pip install -U pip setuptools
# Install packages
RUN pip install -r ./requirements.txt

WORKDIR /src/silver_coin

