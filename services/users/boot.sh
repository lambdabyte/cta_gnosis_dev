#!/bin/sh
export FLASK_DEBUG=1
exec gunicorn -b :5000 --access-logfile - --error-logfile - gnosis:app --reload
