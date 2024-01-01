FROM python:3.9

WORKDIR /app

COPY src/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY src /app/

RUN chmod +x init.sh

EXPOSE 8000
EXPOSE 8001

CMD ["/app/init.sh"]
