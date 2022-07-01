
ARG PY_VER=3.7.13
FROM python:${PY_VER} AS etl-py
MAINTAINER Luis Amilcar Tavares <mikusher@hotmail.com>


RUN mkdir /app \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libpq-dev \
            libsasl2-dev \
            libecpg-dev \
            cron \
    && pip install --upgrade pip

WORKDIR /app

RUN mkdir -p /app/etl/

COPY etl/ /app/etl/
COPY main.py /app/main.py

RUN cd /app \
    && pip install --no-cache -r /app/etl/requirements.txt