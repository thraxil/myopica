#!/bin/bash

cd /var/www/myopica/myopica/
python manage.py migrate --noinput --settings=myopica.settings_docker
python manage.py collectstatic --noinput --settings=myopica.settings_docker
python manage.py compress --settings=myopica.settings_docker
gunicorn --env \
  DJANGO_SETTINGS_MODULE=myopica.settings_docker \
  myopica.wsgi:application -b 0.0.0.0:8000 -w 3 \
  --access-logfile=- --error-logfile=-
