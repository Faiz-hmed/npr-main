#!/bin/bash
gunicorn proj.wsgi:application --bind 0.0.0.0:8000 --timeout $TIMEOUT --workers $WORKERS --log-level info
# python manage.py collectstatic --noinput
# python manage.py runserver 0.0.0.0:8000