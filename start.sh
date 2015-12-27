#!/bin/bash

./manage.py collectstatic --noinput
gunicorn web.wsgi -w 4 -b 0.0.0.0:8000
