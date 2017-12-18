#!/bin/sh

echo "*** Initialize database ***"
[ -f /data/main.cvd ] || freshclam

echo "*** Startup $0 suceeded now starting $@ ***"
exec su-exec clamav "$@"
