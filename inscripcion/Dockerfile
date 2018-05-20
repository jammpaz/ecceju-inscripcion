FROM python:3.6-alpine

ENV FLASK_APP inscripcion.py
ENV FLASK_CONFIG docker

RUN apk --no-cache add build-base postgresql-dev && \
    adduser -D inscripcion

USER inscripcion

WORKDIR /home/inscripcion

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt && \
    venv/bin/pip install psycopg2 psycopg2-binary

COPY app app
COPY domain domain
COPY migrations migrations
COPY utils utils
COPY inscripcion.py config.py boot.sh feature.py features.yaml ./

# runtime configuration
CMD ["./boot.sh"]
