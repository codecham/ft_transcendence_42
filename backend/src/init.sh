#!/bin/bash

python manage.py makemigrations
python manage.py migrate
python manage.py runsslserver --certificate cert.crt --key cert.key 0.0.0.0:8000 &

sleep 5

daphne -e ssl:8001:privateKey=cert\\.key:certKey=cert\\.crt backend.asgi:application
