FROM alpine:latest

RUN echo "@testing http://nl.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories && \
    apk add --update supervisor ca-certificates bash curl \
        # Freeposte AdminUI
        python3-dev libffi-dev openssl-dev build-base \
        # Dovecot Mailserver
        dovecot dovecot-sqlite dovecot-pigeonhole-plugin dovecot-antispam-plugin@testing \
        # Postfix MTA
        postfix postfix-sqlite postfix-pcre \
        # ClamAV Antivirus
        clamav \
        # RSpamD Antispam
        rspamd@testing rspamd-client@testing rmilter@testing redis \
        # Mail Forwarder
        fetchmail && \
    rm -rf /var/cache/apk/*

ADD src /

WORKDIR /app

RUN pip3 install --upgrade pip setuptools && \
    pip install Flask Flask-Login Flask-SQLAlchemy Flask-bootstrap Flask-Babel Flask-migrate Flask-script Flask-wtf WTForms-Components PyOpenSSL passlib gunicorn docker-py tabulate && \
    pybabel compile -d /app/freeposte/translations && \
    # Fix permissions on startup scripts
    chmod -R +x /usr/local/bin/

ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]
