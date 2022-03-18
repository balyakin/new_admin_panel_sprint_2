#!/bin/sh
export DJANGO_SUPERUSER_PASSWORD=admin
# wait postgres to start
sleep 20
cd /app
python manage.py migrate
python manage.py createsuperuser --noinput --username admin --email test@test.com
gunicorn --bind :8000 --workers 3 config.wsgi:application
