# Dockerfile
# We Use an official Python runtime as a parent image
FROM python:3.9-alpine3.13
LABEL maintainer="jacquesonline.com"

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Allows docker to cache installed dependencies between builds

COPY ./requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN python -m venv .venv && \ 
    pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-deps build-base postgresql-dev musl-dev && \
    pip install -r /requirements.txt && \
    apk del .tmp-deps && \
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

USER app