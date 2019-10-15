import os
from flask import Flask
os.system("./start-kafka.sh")
#os.system("/usr/local/kafka/bin/zookeeper-server-start.sh /usr/local/kafka/config/zookeeper.properties")
#os.system("/usr/local/kafka/bin/kafka-server-start.sh /usr/local/kafka/config/server.properties")
#os.system("/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic ai_topic --config retention.ms=10000")
#os.system("/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic cloud_handler_topic --config retention.ms=10000")
#os.system("/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic visualizer_topic --config retention.ms=10000")
#os.system("/usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic broadcaster_topic --config retention.ms=10000")

app = Flask(__name__)

@app.route("/")
def hello_kafka():
    return "ok from kafka container"

if __name__ == '__main__':
    HOST = '0.0.0.0'
    PORT = 8006
    app.run(HOST, PORT, debug=True) 
