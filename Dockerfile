FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
  curl \
  git \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir flask flask-jwt-extended flask-cors sqlalchemy python-dotenv gunicorn

COPY . /app/generator

RUN chmod +x /app/generator/entrypoint.sh

ENTRYPOINT ["/app/generator/entrypoint.sh"]