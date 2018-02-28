FROM python:3

LABEL authors="Danilo Vulicevic danilo.vulicevic@yahoo.com"

ENV SOCIAL_DB_HOST db
COPY ./requirements /social-network/requirements

RUN pip install -r /social-network/requirements/requirements.txt

COPY . /social-network

WORKDIR /social-network
EXPOSE 8000
CMD gunicorn --workers=4 --max-requests 100 -t 200 -b 0.0.0.0:8000 wsgi:application
