#!/bin/sh

echo "*** Summarize variables in config files ***"
find . -name '*.cf' -exec grep -r -o '{{.*}}' {} +

echo "*** Loop all env variables matching the substitution pattern for stage specific configuration ***"
env | while read VARIABLE; do
    echo "*** Set key ${VARIABLE%=*} to value ${VARIABLE#*=} ***"
    sed -i "s|{{ ${VARIABLE%=*} }}|${VARIABLE#*=}|g" /etc/postfix/*.cf
done

# Override Postfix main configuration
if [ -f /overrides/postfix.cf ]; then
  while read line; do
    postconf -e "$line"
  done < /overrides/postfix.cf
  echo "Loaded '/overrides/postfix.cf'"
else
  echo "No extra postfix settings loaded because optional '/overrides/postfix.cf' not provided."
fi

# Override Postfix master configuration
if [ -f /overrides/postfix.master ]; then
  while read line; do
    postconf -Me "$line"
  done < /overrides/postfix.master
  echo "Loaded '/overrides/postfix.master'"
else
  echo "No extra postfix settings loaded because optional '/overrides/postfix.master' not provided."
fi

# Include table-map files
if ls -A /overrides/*.map 1> /dev/null 2>&1; then
  cp /overrides/*.map /etc/postfix/
  postmap /etc/postfix/*.map
  rm /etc/postfix/*.map
  chown root:root /etc/postfix/*.db
  chmod 0600 /etc/postfix/*.db
  echo "Loaded 'map files'"
else
  echo "No extra map files loaded because optional '/overrides/*.map' not provided."
fi

# Actually run Postfix
/usr/lib/postfix/post-install meta_directory=/etc/postfix create-missing

echo "*** Startup $0 suceeded now starting $@ ***"
exec "$@"
