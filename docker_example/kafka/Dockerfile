FROM ubuntu:16.04
 
ENV KAFKA_HOME /usr/local/kafka
ADD ./start-kafka.sh /scripts/
 
# install java + others
RUN apt-get update && apt-get install -y \
  wget \
  openjdk-8-jdk 
 
# install kafka
RUN wget http://www-us.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz 
RUN tar -xzf kafka_2.12-2.2.1.tgz 
RUN mv kafka_2.12-2.2.1 $KAFKA_HOME

WORKDIR /scripts
EXPOSE 2181 9092
CMD ["bash", "start-kafka.sh"] 
