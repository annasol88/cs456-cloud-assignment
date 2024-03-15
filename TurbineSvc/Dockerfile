# syntax=docker/dockerfile:1
FROM python:slim-bullseye
WORKDIR /app
RUN apt update \
    && apt upgrade -y \
    && apt install -y curl \
    && curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11" \
    && apt install -y mariadb-client libmariadb-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ENV PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$PORT app:app"]