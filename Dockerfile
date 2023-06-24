FROM python:3.9-slim

# set the working directory
WORKDIR /app

# create data directory
RUN mkdir data

# copy the Python script and the requirements file
COPY disruptions.py .
COPY .env .
COPY requirements.txt .

# install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# install cron
RUN apt-get update && apt-get -y install cron

# install Filebeat
RUN apt-get update && apt-get -y install curl
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.8.0-linux-x86_64.tar.gz
RUN tar xzvf filebeat-8.8.0-linux-x86_64.tar.gz
RUN mv filebeat-8.8.0-linux-x86_64 /etc/filebeat

# copy the crontab file
COPY crontab /etc/cron.d/my-cron

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron

# apply the cron job
RUN crontab /etc/cron.d/my-cron

# copy the filebeat configuration file
COPY filebeat.yml /etc/filebeat/filebeat.yml

# add the ca certificate
COPY ca.crt /etc/filebeat/certs/ca.crt

# run the command on container startup
CMD service cron start && tail -f /dev/null