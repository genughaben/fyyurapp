#!/bin/sh

echo setting up env $DYNAMIC_ENV_VAR
sudo apt-get update && sudo apt-get install bash
sudo apt-get install -y python-pip
sudo pip install docker-compose
sudo docker image prune -f
sudo docker-compose -f docker-compose.yml build --no-cache
sudo docker-compose -f docker-compose.yml up -d
