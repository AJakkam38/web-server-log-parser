ARG PY_VER=3.8-slim-buster
FROM python:$PY_VER

# Create app directory
WORKDIR /log-parser

# Install app dependencies
ADD requirements.txt .
ADD Makefile .
ADD nginx-log-parser.py .

RUN pip install pytz

RUN cd log-parser