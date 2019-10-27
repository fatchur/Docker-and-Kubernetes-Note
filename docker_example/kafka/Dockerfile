FROM ubuntu:16.04

RUN pwd
ENV KAFKA_HOME /usr/local/kafka
COPY . /scripts/
 
# install java + others
RUN apt-get update && apt-get install -y \
  wget \
  openjdk-8-jdk 
RUN apt-get install -y python3-dev python3-pip
RUN pip3 install flask 
 
# install kafka
RUN wget https://www-eu.apache.org/dist/kafka/2.3.1/kafka_2.12-2.3.1.tgz
RUN tar -xzf kafka_2.12-2.3.1.tgz
RUN mv kafka_2.12-2.3.1 $KAFKA_HOME

EXPOSE 2181 9092 5006
WORKDIR /scripts
RUN pwd
CMD ["python3", "start_kafka.py"] 
