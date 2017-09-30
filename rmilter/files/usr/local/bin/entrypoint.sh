#!/bin/sh

export WHITELIST=$(echo "$RELAYNETS" | sed 's/ /,/g')

echo "*** Loop all env variables matching the substitution pattern for stage specific configuration ***"
env | while read PROPERTY; do
    echo "*** Set key ${PROPERTY%=*} to value ${PROPERTY#*=} ***"
    sed -i "s|{{ ${PROPERTY%=*} }}|${PROPERTY#*=}|g" /etc/rmilter.conf
done

echo ".try_include /etc/rmilter-clamav.conf" >>  /etc/rmilter.conf

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
