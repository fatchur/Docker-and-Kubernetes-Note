FROM ubuntu:16.04

COPY . /scripts/
WORKDIR /scripts

# install dependencies
RUN apt-get update && apt-get install -y \
  wget 
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install -r requirements.txt
RUN apt-get update && apt-get install -y libgtk2.0-dev

WORKDIR /home
EXPOSE 8001
CMD ["python3", "main.py", "2> /dev/null"] 
