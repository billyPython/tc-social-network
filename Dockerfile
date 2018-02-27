FROM python:3

LABEL authors="Danilo Vulicevic danilo.vulicevic@yahoo.com"

RUN apt-get update -y && \
    apt-get install -y \
    python-pip \
    python-dev \
    build-essential \
    libssl-dev \
    libcurl4-openssl-dev \
    apt-utils \
    libffi-dev \
    libxml2-dev \
    libxslt1-dev \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

COPY ./requirements /social-network/requirements

RUN pip install -r /social-network/requirements/requirements.txt

COPY . /social-network

WORKDIR /social-network
EXPOSE 8000
CMD gunicorn --workers=4 --max-requests 100 -t 200 -b 0.0.0.0:8000 wsgi:application
