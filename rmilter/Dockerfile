FROM alpine:edge

RUN set -ex ;\
    echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini rmilter@testing ;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["rmilter", "-n", "-c", "/etc/rmilter.conf"]
