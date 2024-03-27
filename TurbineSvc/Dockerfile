# Base image
FROM python:slim-bullseye
# Working Directory
WORKDIR /app

# Install mariaDB connector to enable connection using MariaDB Driver
RUN apt update 
RUN apt upgrade -y 
RUN apt install -y curl 
RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11"
RUN apt install -y libmariadb-dev gcc 
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*

# Copy everything in working directory into container
COPY . .

# Install Python packages
RUN pip3 install --progress-bar off --upgrade pip 
RUN pip3 install --progress-bar off -r requirements.txt

# Get the certificate needed for SSL connection.
#RUN curl -s -O https://cacerts.digicert.com/DigiCertGridCA-1.crt.pem


# Set port number if not provided
ENV SVC_PORT=5000

# Start gunicord server attaching to the create() function in app.py
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:$SVC_PORT 'app:create()'"]
