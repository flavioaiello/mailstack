#!/bin/sh

echo "*** Upgrading database ***"
python manage.py db upgrade

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
