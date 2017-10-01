FROM alpine:edge

RUN set -ex ;\
    echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini dovecot dovecot-sqlite dovecot-pigeonhole-plugin dovecot-pigeonhole-plugin-extdata rspamd-client@testing;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["/usr/sbin/dovecot", "-c", "/etc/dovecot/dovecot.conf", "-F"]
