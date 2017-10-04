FROM python:3-alpine3.6

COPY files /

WORKDIR /app

RUN set -ex;\
    apk update;\
    apk upgrade;\
    apk add --no-cache --virtual .build-deps;\
    apk add --no-cache su-exec tini openssl openssl-dev libffi-dev python-dev build-base;\
    pip install -r requirements.txt;\
    apk del .build-deps;\
    rm -rf /var/cache/apk/*;\
    pybabel compile -d mailu/translations

ENTRYPOINT ["/sbin/tini", "--", "entrypoint.sh"]
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "--access-logfile", "-", "--error-logfile", "-", "--preload", "mailu:app"]
