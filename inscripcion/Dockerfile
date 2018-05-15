FROM python:3.6-alpine

ENV FLASK_APP inscripcion.py
ENV FLASK_CONFIG docker

RUN adduser -D inscripcion
USER inscripcion

WORKDIR /home/inscripcion

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY domain domain
COPY migrations migrations
COPY inscripcion.py config.py boot.sh feature.py features.yaml ./

# runtime configuration
ENTRYPOINT ["./boot.sh"]
