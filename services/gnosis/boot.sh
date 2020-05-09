#!/bin/sh
export FLASK_APP=gnosis.py
export FLASK_DEBUG=1

ls -a ~/
until flask db upgrade
  do
      exec flask db upgrade
  done


exec gunicorn -b :5000 --access-logfile - --error-logfile - gnosis:app --reload


