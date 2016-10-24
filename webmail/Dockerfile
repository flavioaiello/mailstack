FROM php:5-apache

ENV ROUNDCUBE_VERSION 1.2.2

RUN apt-get update && \
    apt-get install -y libfreetype6-dev libjpeg62-turbo-dev libmcrypt-dev libpng12-dev && \
    docker-php-ext-install pdo_mysql mcrypt

ADD src /

WORKDIR /var/www/html

RUN curl -sSL https://github.com/roundcube/roundcubemail/releases/download/${ROUNDCUBE_VERSION}/roundcubemail-${ROUNDCUBE_VERSION}-complete.tar.gz | tar -C /var/www/html -xvz --strip-components=1 roundcubemail-${ROUNDCUBE_VERSION} && \
    chown -R www-data:www-data temp logs && \
    chmod -R +x /usr/local/bin

ENTRYPOINT ["/usr/local/bin/run.sh"]
CMD ["apache2-foreground"]
