## Kafka
![](assets/kafka.png)

### Installing Kafka on 
- `sudo apt update` and  `sudo apt install default-jdk`
- get the package: `wget http://www-us.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz`
- extract: `tar xzf kafka_2.12-2.2.1.tgz`
- move to: `mv kafka_2.12-2.2.1 /usr/local/kafka`
- `cd /usr/local/kafka`


### Starting-up Kafka Zoookeeper and Kafka server
- start zookeeper: `bin/zookeeper-server-start.sh config/zookeeper.properties`
- start kafka: `bin/kafka-server-start.sh config/server.properties`


### Create Topic and Test
- create topic: `bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic <topic_name>`
- see the created topic: `bin/kafka-topics.sh --list --zookeeper localhost:2181`
- get the topic description: `bin/kafka-topics.sh --describe --zookeeper localhost:2181 --topic <topic name>`
- sending a message: `bin/kafka-console-producer.sh --broker-list localhost:9092 --topic <topic_name>`
- consume the message: `bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic <topic name> --from-beginning`

if you want to delete the kafka topic,
- `bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic <topic name>`


### Kafka Retention and Deletion Policy
1. Time Based Retention: Under this policy, we configure the maximum time a Segment (hence messages) can live for. Once a Segment has spanned configured retention time, it is marked for deletion or compaction depending on configured cleanup policy. Default retention time for Segments is 7 days. example
```
# add this to your topic creation command
--config retention.ms=8640000 
```

2. Size based Retention: In this policy, we configure the maximum size of a Log data structure for a Topic partition. Once Log size reaches this size, it starts removing Segments from its end. This policy is not popular as this does not provide good visibility about message expiry. However it can come handy in a scenario where we need to control the size of a Log due to limited disk space.
```
# add this to your topic creation command
log.retention.bytes=104857600
```


### Note
- The default port of zookeeper: 2181
- The default port for kafka server: 9092
- **kafka concepts**:  

Kafka is depending on the zookeeper, so starting up the zookeeper first before starting the kafka. There are three components in kafka, producer, topic, and consumer.
1. producer: produceing a message to the topic
2. topic: the bridge between producer and consumer
3. consumer: consuming messages from topic

The usual port for zookeeper is `2181` and `9092` for kafka.  Before doing the streaming or messaging job, we have to make `kafka topic` fisrt. 

Kafka producer created by this example code,
```python
# -------------------------- #
# x can be a string, int, list or python dictionary  
# -------------------------- #
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                         value_serializer=lambda x: 
                         dumps(x).encode('utf-8'))
```

for sending a message, we can use this example,
```python
# -------------------------- #
# numtest is the topic name  #  
# -------------------------- #
data = {'number' : 2}
producer.send('numtest', value=data)
```

Kafka consumer will consume the message via `topic`. 
```python
# -------------------------- #
# numtest is the topic name  #  
# -------------------------- #
from kafka import KafkaConsumer
consumer = KafkaConsumer(
                        'numtest',
                        bootstrap_servers=['localhost:9092'],
                        auto_offset_reset='earliest',
                        enable_auto_commit=True,
                        group_id='my-group',
                        value_deserializer=lambda x: loads(x.decode('utf-8')))
```
There are some important arguments here:
1. `auto_offset_reset`, It handles where the consumer starts reading the message after breaking down. if this argument is set as `earliest`, the consumer will get the earliest message in the `topic`. The benefit is there are no data losts. But if we set it as `latest`, the consumer will get the latest data, so there are some data losts.
2. `enable_auto_commit`: boolean, autocommit for the producer.
3. `auto_commit_interval_ms`: the minimum time for consumer to commit the message. If the consumer down after consuming the message and the time interval belows `auto_commit_interval_ms`, the kafka will assume that the message is never consumed by producer (never committed).
4. `group_id`: the consumer group to which the consumer belongs. Remember from the introduction that a consumer needs to be part of a consumer group to make the auto commit work.

Example of consuming message:
```python 
   for message in consumer:
        message = message.value
        print (message)
```

## Running Kafka Docker
`sudo docker run --name <container name> -d -p 9092:9092 -p 2181:2181 --network=host <image name>:<tag>`







