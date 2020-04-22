FROM python:3.6-alpine

RUN adduser -D gnosis

WORKDIR /home/gnosis/services/gnosis

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN pip install --upgrade setuptools
RUN apk update && \
    apk add --virtual build-deps && \
    apk add postgresql-dev gcc python3-dev musl-dev && \
    apk add netcat-openbsd && \
    apk add --update nodejs && \
    apk add yarn
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY /app ./app
COPY gnosis.py boot.sh ./
RUN chmod +x boot.sh
RUN chmod +x gnosis.py

ENV FLASK_APP gnosis.py


RUN chown -R gnosis:gnosis ./
USER gnosis

EXPOSE 5000
EXPOSE 5432
ENTRYPOINT ["./boot.sh"]