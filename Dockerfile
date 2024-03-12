FROM python:3.10.3
RUN apt-get update && apt-get -y install cron vim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt
COPY crontab /etc/cron.d/crontab
COPY audot.py ./audot.py
RUN chmod 0644 /etc/cron.d/crontab
RUN /usr/bin/crontab /etc/cron.d/crontab

# run crond as main process of container
CMD ["cron", "-f"]


