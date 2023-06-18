FROM python:3.9-slim

# set the working directory
WORKDIR /app

# copy the Python script and the requirements file
COPY disruptions.py .
COPY .env .
COPY requirements.txt .

# install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# install cron
RUN apt-get update && apt-get -y install cron

# copy the crontab file
COPY crontab /etc/cron.d/my-cron

# give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron

# apply the cron job
RUN crontab /etc/cron.d/my-cron

# run the command on container startup
CMD ["cron", "-f"]