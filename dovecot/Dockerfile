FROM alpine:3.7

RUN set -ex ;\
    apk update;\
    apk upgrade;\
    apk add --no-cache su-exec tini dovecot dovecot-sqlite dovecot-pigeonhole-plugin dovecot-pigeonhole-plugin-extdata rspamd-client;\
    rm -rf /var/cache/apk/*

COPY files /

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["/usr/sbin/dovecot", "-c", "/etc/dovecot/dovecot.conf", "-F"]
