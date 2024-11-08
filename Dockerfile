FROM python:3.9-slim

WORKDIR /app

COPY connect21/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

