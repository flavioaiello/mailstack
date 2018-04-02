FROM alpine:edge

# Add local files to image
COPY files /

# Packages
RUN set -ex ;\
    apk update ;\
    apk upgrade ;\
    apk add --no-cache mariadb mariadb-client pwgen ;\
    rm -rf /var/cache/apk/* ;\
    mkdir -p /run/mysqld ;\
    chown -R mysql:mysql /run/mysqld ;\
    sed -Ei 's/^(bind-address|log)/#&/' /etc/mysql/my.cnf ;\
    sed -i '/^\[mysqld]$/a skip-host-cache\nskip-name-resolve' /etc/mysql/my.cnf

VOLUME ["/var/lib/mysql"]

EXPOSE 3306

ENTRYPOINT ["entrypoint.sh"]
CMD ["mysqld","--user=mysql","--console"]
