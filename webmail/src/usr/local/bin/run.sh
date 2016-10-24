#!/bin/sh

chown -R www-data:www-data /data

exec "$@"
