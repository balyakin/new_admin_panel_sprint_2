#!/bin/sh
while ! nc -z $DB_HOST 5432; do sleep 1; done;
cd /app
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email test@test.com
gunicorn --bind :8000 --workers 3 config.wsgi:application
