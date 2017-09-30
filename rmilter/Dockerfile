FROM alpine:edge

COPY files /

RUN set -ex ;\
    echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini rmilter@testing ;\
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["rmilter", "-n", "-c", "/etc/rmilter.conf"]
