#syntax=docker/dockerfile:1.2
FROM python:3.9.5-alpine AS alpine_base
  ENV PYTHONDONTWRITEBYTECODE=1
  RUN true \
    && mkdir -p /srv/app \
    && addgroup -S app \
    && adduser -HDS -h /srv -G app app \
    && chown -R app:app /srv \
    && mkdir -p /wheel \
    && chown -R app:app /wheel \
    ;

  RUN true \
    && apk add --no-cache --update \
      build-base \
      postgresql-dev \
      python3-dev \
    ;

  RUN pip install \
    --no-cache-dir \
    --disable-pip-version-check \
    pipenv \
    ;

  USER app
  WORKDIR /srv/app

FROM alpine_base as pip_base
  COPY --chown=app:app . /srv/app
  RUN pipenv sync --clear
  ENTRYPOINT ["pipenv", "run"]

FROM pip_base as dev
  RUN pipenv sync -d \
    && pipenv --clear
