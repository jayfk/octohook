FROM python:3.5-slim
ENV PYTHONUNBUFFERED 1

ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD hook /app/hook
ADD repos /app/repos

WORKDIR /app/hook