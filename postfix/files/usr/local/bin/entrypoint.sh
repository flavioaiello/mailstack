#!/bin/sh

echo "*** Loop all env variables matching the substitution pattern for stage specific configuration ***"
env | while read VARIABLE; do
    echo "*** Set key ${VARIABLE%=*} to value ${VARIABLE#*=} ***"
    sed -i "s|{{ ${VARIABLE%=*} }}|${VARIABLE#*=}|g" /etc/postfix/*.cf
done

# Postfix postinstall procedure
/usr/lib/postfix/post-install meta_directory=/etc/postfix create-missing
postmap /etc/postfix/without_ptr
newaliases

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
