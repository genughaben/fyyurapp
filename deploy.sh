#!/bin/sh

echo setting up env $DYNAMIC_ENV_VAR
apk update && apk add sudo
sudo apk update && sudo apk bash
sudo apk add --update py-pip
sudo pip install docker-compose
sudo docker image prune -f
sudo docker-compose -f docker-compose.yml build --no-cache
sudo docker-compose -f docker-compose.yml up -d
