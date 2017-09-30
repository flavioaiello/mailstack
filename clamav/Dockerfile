FROM alpine:edge

RUN set -ex ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini clamav rsyslog wget clamav-libunrar ;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["clamd"]

