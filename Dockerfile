FROM python:3.6.9
MAINTAINER genughaben

ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /requirements.txt

# Setup directory structure
ADD . /code
WORKDIR /code

RUN useradd -ms /bin/bash user
USER user

CMD ["bash", "start.sh"]
