FROM python:3.6-alpine

RUN adduser -D gnosis

WORKDIR /home/gnosis/services/users

COPY requirements.txt requirements.txt
RUN pip install -U pip
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt
RUN pip install gunicorn

COPY app app
COPY gnosis.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP gnosis.py


RUN chown -R gnosis:gnosis ./
USER gnosis

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]