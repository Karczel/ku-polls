#!/bin/sh
python3 ./manage.py makemigrations

python3 ./manage.py migrate

python3 ./manage.py loaddata data/polls-v4.json data/users.json data/votes-v4.json

python3 ./manage.py runserver 0.0.0.0:8000