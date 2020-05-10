import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database

# app started outside_docker using postgres in docker or local
SQLALCHEMY_DATABASE_URI = 'postgres://postgres:docker@localhost:5432/fyyur'

# check if app started inside docker, thus using docker postgres from inside as outlined in docker-compose.yml
docker = False
if 'DOCKER' in os.environ:
    if os.environ['DOCKER'] == 'True':
        SQLALCHEMY_DATABASE_URI = 'postgres://postgres:docker@fyyurdb:5432/fyyur'
