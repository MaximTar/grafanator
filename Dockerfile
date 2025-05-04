FROM python:3.12-bullseye

RUN apt-get update \
    && apt-get upgrade -y \
    && pip install --upgrade pip \
    && apt-get clean

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./src /app/src

COPY ./tests /app/tests
COPY pytest.ini /app/pytest.ini

ENV PYTHONPATH=/app
