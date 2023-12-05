# Use this command at this directory
# docker build -t yourImageName -f Dockerfile .
# docker run -it --net=host --gpus all --name containerName imageName

# Use this command in container
# cd /benchmarkDCC/linear_road
# sh generator.sh

FROM ubuntu:20.04

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON=/usr/bin/python

RUN apt-get update \
    && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get install -y git vim build-essential libssl-dev libffi-dev python-dev wget zip python3 python3-pip default-jdk scala net-tools iputils-ping \
    && git clone https://github.com/walmartlabs/LinearGenerator.git \
    && git clone https://github.com/GoRyne/benchmarkDCC.git \
    && wget https://archive.apache.org/dist/spark/spark-3.2.3/spark-3.2.3-bin-hadoop3.2.tgz \
    && wget --no-check-certificate https://archive.apache.org/dist/kafka/2.5.0/kafka_2.12-2.5.0.tgz \
    && mkdir /opt/spark && mkdir /data && mkdir /data/datasets \
    && pip install kafka-python\
    && tar -xf spark-3.2.3-bin-hadoop3.2.tgz -C /opt/spark --strip-component 1 \
    && tar -xzvf kafka_2.12-2.5.0.tgz -C /usr/local/src/ \
    && echo "\nlisteners=PLAINTEXT://:9092" >> /usr/local/src/kafka_2.12-2.5.0/config/server.properties \
    && echo "\nadvertised.listeners=PLAINTEXT://localhost:9092" >> /usr/local/src/kafka_2.12-2.5.0/config/server.properties 