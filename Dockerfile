FROM python:3.10-alpine AS base

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apk add --update --no-cache postgresql-client jpeg-dev
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev musl-dev zlib zlib-dev

FROM base AS dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

FROM dependencies AS run
RUN mkdir /app
WORKDIR /app
COPY . .