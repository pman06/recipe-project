FROM python:3.9

ENV PYTHONDONTWRITEBYTECODES 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /code
WORKDIR /code


COPY Pipfile Pipfile.lock /code/

RUN pip install pipenv && pipenv install --system

COPY . /code
