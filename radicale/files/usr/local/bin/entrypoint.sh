#!/bin/sh

echo "*** Loop all env variables matching the substitution pattern for stage specific configuration ***"
env | while read PROPERTY; do
    echo "*** Set key ${PROPERTY%=*} to value ${PROPERTY#*=} ***"
    sed -i "s|{{ ${PROPERTY%=*} }}|${PROPERTY#*=}|g" /etc/dovecot/*.conf
done

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
