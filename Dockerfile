FROM python:3.9-rc-alpine3.12
MAINTAINER bondeveloper

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
COPY ./app /app
WORKDIR /app

# RUN adduser -D bondeveloper

# RUN addgroup -g 1001 www-data
# RUN adduser -D -u 1001 -G www-data bondeveloper

# COPY --chown=bondeveloper:www-data . /app

# USER bondeveloper

RUN adduser -D bondeveloper
USER bondeveloper
