FROM ubuntu:16.04

COPY . /scripts/
WORKDIR /scripts

# install dependencies
RUN apt-get update && apt-get install -y wget 
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgtk2.0-dev

WORKDIR /home/cloud_handler/
EXPOSE 8004
CMD ["gunicorn", "-k", "gevent", "-w", "1", "-b", "0.0.0.0:8004", "main:app"] 

