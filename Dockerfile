FROM python:3.11.0-slim-bullseye

# Install cron & curl
RUN apt-get update && \
    apt-get install -y curl cron && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install Filebeat
RUN curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-8.8.0-amd64.deb && \
    dpkg -i filebeat-8.8.0-amd64.deb && \
    rm filebeat-8.8.0-amd64.deb

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

# copy the cron file to the cron.d directory
COPY cronfile /etc/cron.d/cronfile

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/cronfile

# apply cron job
RUN crontab /etc/cron.d/cronfile

# CMD run cron and filebeat
CMD cron && filebeat -e -c /etc/filebeat/filebeat.yml