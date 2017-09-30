FROM alpine:edge

COPY files /

RUN set -ex ;\
    echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini rspamd@testing ca-certificates;\
    rm -rf /var/cache/apk/*;\
    mkdir /run/rspamd

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["rspamd", "-u", "rspamd", "-g", "rspamd", "-f"]
