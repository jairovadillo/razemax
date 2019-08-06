FROM python:3.7-alpine

RUN apk update
RUN apk add curl bash

COPY tests/config/requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app

WORKDIR /app
