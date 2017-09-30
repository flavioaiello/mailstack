#!/bin/sh

echo "*** Fix permisssions ***"
chown -R www-data:www-data /data

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
