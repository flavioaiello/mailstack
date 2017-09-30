FROM python:alpine

RUN set -ex ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini fetchmail ca-certificates;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "fetchmail.py"]
