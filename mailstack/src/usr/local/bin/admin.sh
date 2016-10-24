#!/bin/sh
python3 manage.py db upgrade
python3 manage.py admin postmaster $DOMAIN $SECRET_KEY
exec gunicorn -w 4 -b 0.0.0.0:80 --access-logfile - --error-logfile - --chdir /app freeposte:app
