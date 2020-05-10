echo "BEGIN - docker-var:"
echo $DOCKER
echo "END - docker-var."
GUNICORN_CMD_ARGS="--bind=0.0.0.0:7001 --workers=1 --log-file=- --reload" gunicorn app:app -e PYTHONUNBUFFERED='True' -e DOCKER='True'
