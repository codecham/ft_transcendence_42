FROM python:3.9

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

EXPOSE 8000
