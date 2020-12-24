FROM python:3.9-rc-alpine3.12


ENV PATH="/scripts:${PATH}"
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
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

# RUN addgroup -g 1001 www-data
# RUN adduser -D -u 1001 -G www-data bondeveloper
# COPY --chown=bondeveloper:www-data . /app

RUN adduser -D bondeveloper
RUN chown -R bondeveloper:bondeveloper  /vol
RUN chmod -R 755 /vol/web

USER bondeveloper

CMD ["entrypoint.sh"]
