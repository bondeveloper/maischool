FROM python:3.9-rc-alpine3.12
MAINTAINER bondeveloper

ENV PYTHONUNBUFFERED 1
ARG CACHEBUST=1

RUN pip install --upgrade pip

COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
  gcc libc-dev linux-headers postgresql-dev
RUN apk add --update --no-cache libressl-dev musl-dev libffi-dev


RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps


RUN mkdir /app
COPY ./app /app
WORKDIR /app

# RUN adduser -D bondeveloper

#RUN addgroup -g 1001 www-data
#RUN adduser -D -u 1001 -G www-data bondeveloper

#COPY --chown=bondeveloper:www-data . /app

#USER bondeveloper

RUN adduser -D bondeveloper
USER bondeveloper
