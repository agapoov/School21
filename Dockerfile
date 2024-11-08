FROM python:3.9-slim

WORKDIR /app

COPY connect21/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python connect21/manage.py migrate && python connect21/manage.py runserver 0.0.0.0:8000"]
