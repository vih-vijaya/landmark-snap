#!/bin/bash
python manage.py migrate --noinput
gunicorn landmark_backend.wsgi --bind=0.0.0.0:$PORT
