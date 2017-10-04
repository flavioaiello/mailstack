#!/bin/sh

echo "*** Initialize database ***"
[ -f /data/main.cvd ] || freshclam

echo "*** Start update agent in background mode ***"
freshclam -d -c 6

echo "*** Startup $0 suceeded now starting $@ ***"
exec su-exec clamav "$@"
