#!/bin/bash
export PORT=${PORT:-5000}
export PYTHONUNBUFFERED=1
gunicorn --bind 0.0.0.0:$PORT --workers 2 --timeout 60 wsgi:app
