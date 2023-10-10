FROM python:3.11-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY app app
COPY migrations migrations
COPY impserv.py config.py tests.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP impserv.py

ENTRYPOINT ["./boot.sh"]