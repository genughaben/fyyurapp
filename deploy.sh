#!/bin/sh

echo setting up env $DYNAMIC_ENV_VAR
apk update && apk add sudo
apk add --update py-pip
pip install -U setuptools
apk add python-dev libffi-dev openssl-dev gcc libc-dev make
pip install --upgrade pip
pip install docker-compose
docker image prune -f
docker-compose -f docker-compose.yml build --no-cache
docker-compose -f docker-compose.yml up -d
