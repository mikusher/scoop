
ARG PY_VER=3.8-slim
FROM python:${PY_VER} AS etl-py
MAINTAINER Luis Amilcar Tavares <mikusher@hotmail.com>

# set a environment variable to enviroment variable
ENV PRODUCTION=True

RUN groupadd --gid 1000 user && \
    useradd --uid 1000 --gid 1000 --create-home --shell /bin/bash user

RUN mkdir -p /home/user/app \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libpq-dev \
            libsasl2-dev \
            libecpg-dev \
            cron \
    && pip install --upgrade pip


COPY ../millennium/ /home/user/app/millennium


RUN cd /home/user/app/millennium \
    && pip install --no-cache-dir -r requirements.txt

RUN chown -R "1000:1000" /home/user
USER user
WORKDIR /home/user/app