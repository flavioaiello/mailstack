#!/bin/sh

echo "*** Startup $0 suceeded now starting $@ ***"
exec su-exec clamav "$@"
