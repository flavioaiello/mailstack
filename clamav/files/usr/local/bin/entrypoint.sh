#!/bin/sh

echo "*** Bootstrap the database if clamav is running for the first time ***"
[ -f /data/main.cvd ] || freshclam

echo "*** Run the update daemon ***"
freshclam -d -c 6

echo "*** Startup $0 suceeded now starting $@ ***"
exec su-exec clamav "$@"
