# Base Image
FROM mcr.microsoft.com/azure-functions/python:4-python3.11

# Azure environment variables
ENV AzureWebJobsScriptRoot=/home/site/wwwroot \
    AzureFunctionsJobHost__Logging__Console__IsEnabled=true

# Install mariaDB connector to enable connection using MariaDB Driver
RUN apt update 
RUN apt upgrade -y 
RUN apt install -y curl 
RUN curl -LsS https://r.mariadb.com/downloads/mariadb_repo_setup | bash -s -- --mariadb-server-version="mariadb-10.11"
RUN apt install -y libmariadb-dev gcc 
RUN apt-get clean 
RUN rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /
RUN pip3 install --progress-bar off --upgrade pip 
RUN pip3 install --progress-bar off -r requirements.txt

# Download certificate needed for SSL connection
#RUN curl -s -O https://cacerts.digicert.com/DigiCertGridCA-1.crt.pem

# Copy code to the AzureWebJobsScriptRoot set above
COPY . /home/site/wwwroot
