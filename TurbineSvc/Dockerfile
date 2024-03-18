FROM python:slim-bullseye
WORKDIR /app
RUN apt update 
RUN apt upgrade -y 
RUN apt install -y curl 
RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11"
RUN apt install -y libmariadb-dev gcc 
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*
COPY . .
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt
ENV SVC_PORT=5000
CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:$SVC_PORT app:app"]
