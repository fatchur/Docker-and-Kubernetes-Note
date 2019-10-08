#!/bin/bash
 
# start zookeeper
/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties &
 
# start kafka broker
/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties &

# create ai_topic
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ai_topic --config retention.ms=10000 &
# create cloud_handler topic
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic cloud_handler_topic --config retention.ms=10000 &
# create visualizer_topic
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic visualizer_topic --config retention.ms=10000 &
# create broadcaster_topic
/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic broadcaster_topic --config retention.ms=10000 &
wait