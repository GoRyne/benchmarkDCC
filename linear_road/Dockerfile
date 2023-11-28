# Use this command at this directory
# docker build -t yourImageName -f Dockerfile .
# docker run -it --net=host --gpus all --name containerName imageName

# Use this command in container
# start-master.sh                                                                                                                       -> for spark master
# sh /usr/local/src/kafka_2.12-2.5.0/bin/zookeeper-server-start.sh -daemon /usr/local/src/kafka_2.12-2.5.0/config/zookeeper.properties  -> for zookeeper
# sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-server-start.sh -daemon /usr/local/src/kafka_2.12-2.5.0/config/server.properties         -> for kafka
# sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-topics.sh --create --topic test --bootstrap-server localhost:9092                        -> to make topic
# sh /usr/local/src/kafka_2.12-2.5.0/bin/kafka-console-producer.sh --topic test --bootstrap-server localhost:9092                       -> to make messages
# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0                                                               -> for spark shell

FROM ubuntu:20.04

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON=/usr/bin/python

RUN apt-get update \
    && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get install -y git vim build-essential libssl-dev libffi-dev python-dev wget zip python3 python3-pip default-jdk scala net-tools iputils-ping \
    && git clone https://github.com/walmartlabs/LinearGenerator.git \
    && wget https://archive.apache.org/dist/spark/spark-3.2.3/spark-3.2.3-bin-hadoop3.2.tgz \
    && wget --no-check-certificate https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz \
    && mkdir /opt/spark \
    && tar -xf spark-3.2.3-bin-hadoop3.2.tgz -C /opt/spark --strip-component 1 \
    && tar -xzvf kafka_2.12-2.5.0.tgz -C /usr/local/src/ \
    && echo "\nlisteners=PLAINTEXT://:9092" >> /usr/local/src/kafka_2.12-2.5.0/config/server.properties \
    && echo "\nadvertised.listeners=PLAINTEXT://localhost:9092" >> /usr/local/src/kafka_2.12-2.5.0/config/server.properties 