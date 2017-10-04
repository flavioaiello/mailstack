FROM php:5-apache

COPY files /

ENV RC_VERSION 1.2.3

RUN apt-get update;\
    apt-get upgrade -y;\
    apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev;\
    docker-php-ext-install pdo_mysql mcrypt

RUN echo date.timezone=UTC > /usr/local/etc/php/conf.d/timezone.ini;\
    curl -sSL https://github.com/roundcube/roundcubemail/releases/download/${RC_VERSION}/roundcubemail-${RC_VERSION}-complete.tar.gz | tar -C /var/www/html/ -xvz --strip-components=1 roundcubemail-${RC_VERSION} ;\
    rm -rf CHANGELOG INSTALL LICENSE README.md UPGRADING composer.json-dist installer ;\
    chown -R www-data: logs

ENTRYPOINT ["entrypoint.sh"]
CMD ["apache2-foreground"]
