FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/etl

RUN python -m pip install --upgrade pip
RUN pip install --upgrade setuptools
COPY requirements.txt /usr/etl/requirements.txt
RUN pip install -r /usr/etl/requirements.txt

COPY . .

CMD python3 etl.py