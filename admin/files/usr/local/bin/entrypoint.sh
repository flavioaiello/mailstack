#!/bin/sh

echo "*** Upgrading database ***"
python manage.py db upgrade

echo "*** Setup admin user ***"
python manage.py admin ${USERNAME} ${DOMAIN} ${PASSWORD}

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
