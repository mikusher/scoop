
MAINTAINER Luis Amilcar Tavares <mikusher@hotmail.com>

ARG PY_VER=3.8.12
FROM python:${PY_VER} AS etl-py

RUN mkdir /app \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libpq-dev \
            libsasl2-dev \
            libecpg-dev \
            cron

RUN pip install --upgrade pip

WORKDIR /app

COPY . .

RUN cd /app \
    && pip install --no-cache -r /app/etl/requirements.txt