FROM python:3.12-alpine3.19

RUN apk add --no-cache build-base postgresql-dev
RUN pip install --upgrade pip

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt --no-cache-dir

COPY . /app