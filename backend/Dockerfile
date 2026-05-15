FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential curl libpq-dev postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements/ /app/requirements/
ARG REQUIREMENTS_FILE=local.txt
RUN pip install --upgrade pip \
    && pip install -r requirements/${REQUIREMENTS_FILE}

COPY . /app/

RUN mkdir -p /app/staticfiles /app/media /logs/django /logs/celery /logs/audit

EXPOSE 8000
CMD ["gunicorn", "config.wsgi:application", "--config", "config/gunicorn.conf.py"]
