FROM python:3.10

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /usr/src

RUN pip install --upgrade pip
COPY requirements.txt /usr/src/requirements.txt
RUN pip install -r /usr/src/requirements.txt

COPY . .
EXPOSE 8003
ARG CONF_PATH=core/gunicorn_conf.py

CMD gunicorn --config core/gunicorn_conf.py -k uvicorn.workers.UvicornWorker main:app

