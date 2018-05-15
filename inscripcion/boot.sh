#!/bin/sh
source venv/bin/activate
flask deploy
exec gunicorn -b :$PORT --access-logfile - --error-logfile - inscripcion:app
