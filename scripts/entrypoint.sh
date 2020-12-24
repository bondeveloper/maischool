#!/bin/sh

set -e

python manage.py collectstatic --noinput

python manage.py wait_for_db &&
                    python manage.py makemigrations &&
                    python manage.py migrate &&

uwsgi --socket :8000 --master --enable-threads --module maischool.wsgi