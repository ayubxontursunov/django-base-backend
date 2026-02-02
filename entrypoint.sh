#!/bin/sh
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn core.wsgi:application --bind 0.0.0.0:${WEB_PORT} --workers=12 --timeout 3000
