FROM alpine:edge

RUN set -ex ;\
    echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini radicale@testing py-dulwich@testing;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["radicale", "-f", "-S", "-C", "/radicale.conf"]
