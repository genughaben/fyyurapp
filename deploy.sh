#!/bin/sh

echo setting up env $DYNAMIC_ENV_VAR
docker-compose down
docker image prune -f
docker-compose -f docker-compose.yml build --no-cache
docker-compose -f docker-compose.yml up -d
