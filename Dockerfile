FROM python:2-alpine

# Install Docker
RUN apk add docker

# Install Docker Compose
RUN pip install docker-compose

# Install Git
RUN apk add git

ADD . /src
WORKDIR /src

# Install Hokusai
RUN pip install .
