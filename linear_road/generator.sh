#!/bin/sh

start-master.sh                                                                                                                      # -> for spark master
sh /usr/local/src/kafka_2.12-2.5.0/bin/zookeeper-server-start.sh -daemon /usr/local/src/kafka_2.12-2.5.0/config/zookeeper.properties # -> for zookeeper
sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-server-start.sh -daemon /usr/local/src/kafka_2.12-2.5.0/config/server.properties        # -> for kafka
sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-topics.sh --create --topic linear-road-topic --bootstrap-server localhost:9092          # -> to make topic
# sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-console-producer.sh --topic linear-road-topic --bootstrap-server localhost:9092       # -> to make messages
# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0                                                            # -> for spark shell
# sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-console-consumer.sh --topic linear-road-topic --bootstrap-server localhost:9092       # -> to consume messages   
cd /LinearGenerator/src
javac com/walmart/linearroad/generator/*.java
nohup java com.walmart.linearroad.generator.LinearGen -x 10 -m 8 1>/data/datasets/output_0 2>/data/datasets/error_0 &
cd /benchmarkDCC/linear_road
python3 normal_avg.py 100 2