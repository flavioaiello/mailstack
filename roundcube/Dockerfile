FROM php:5-apache

COPY files /

ENV ROUNDCUBE_URL https://github.com/roundcube/roundcubemail/releases/download/1.2.3/roundcubemail-1.2.3-complete.tar.gz

RUN apt-get update;\
    apt-get upgrade -y;\
    apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev;\
    docker-php-ext-install pdo_mysql mcrypt

RUN echo date.timezone=UTC > /usr/local/etc/php/conf.d/timezone.ini;\
    curl -sSL ${ROUNDCUBE_URL} | tar -C /var/www/html/ -xvz --strip-components=1 roundcubemail-1.2.3 ;\
    rm -rf CHANGELOG INSTALL LICENSE README.md UPGRADING composer.json-dist installer ;\
    chown -R www-data: logs

ENTRYPOINT ["entrypoint.sh"]
CMD ["apache2-foreground"]
