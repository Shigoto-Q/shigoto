FROM python:3.8-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  && apt-get install -y build-essential \
  && apt-get install -y libpq-dev \
  && apt-get install -y gettext \
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get install gnupg2 -y \
  && apt-get install curl -y \
  && apt-get install git -y \
  && apt-get install nodejs -y \
  && apt-get install npm -y \
  && rm -rf /var/lib/apt/lists/* \

COPY ./package.json /package.json
COPY ./package-lock.json /package-lock.json

RUN npm install

RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] http://packages.cloud.google.com/apt cloud-sdk main" | \
tee -a /etc/apt/sources.list.d/google-cloud-sdk.list  \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg |  \
    apt-key --keyring /usr/share/keyrings/cloud.google.gpg  add -  \
    && apt-get update -y  \
    && apt-get install google-cloud-sdk -y
RUN apt-get install kubectl

COPY ./requirements /requirements
RUN pip install -r /requirements/local.txt

COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./compose/local/django/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r$//g' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r$//g' /start-flower
RUN chmod +x /start-flower



WORKDIR /app

ENTRYPOINT ["/entrypoint"]
