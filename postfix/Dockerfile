FROM alpine:edge

COPY files /

RUN set -ex ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini postfix postfix-sqlite postfix-pcre ;\
    rm -rf /var/cache/apk/*

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["/usr/lib/postfix/master", "-c", "/etc/postfix", "-d"]
