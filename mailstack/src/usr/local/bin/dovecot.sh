#!/bin/bash

# Substitute configuration
for VARIABLE in `env | cut -f1 -d=`; do
  sed -i "s={{ $VARIABLE }}=${!VARIABLE}=g" /etc/dovecot/*.conf
done

# Run dovecot
exec /usr/sbin/dovecot -c /etc/dovecot/dovecot.conf -F
