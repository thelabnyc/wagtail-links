FROM python:3.7
ENV PYTHONUNBUFFERED 0

RUN mkdir /code
WORKDIR /code

ADD requirements.txt /code/
RUN pip install -r requirements.txt

