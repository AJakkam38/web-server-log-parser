ARG PY_VER=3.8-slim-buster
FROM python:$PY_VER

# Create app directory
RUN mkdir -p /log-parser
WORKDIR /log-parser

# Install app dependencies
ADD Makefile /log-parser/Makefile
ADD nginx-log-parser.py /log-parser/nginx-log-parser.py

RUN pip install pytz

RUN cd log-parser