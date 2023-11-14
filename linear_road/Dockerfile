FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get install -y git vim build-essential libssl-dev libffi-dev python-dev wget zip python3 python3-pip default-jdk scala

RUN wget https://archive.apache.org/dist/spark/spark-3.2.3/spark-3.2.3-bin-hadoop3.2.tgz \
    && mkdir /opt/spark \
    && tar -xf spark-3.2.3-bin-hadoop3.2.tgz -C /opt/spark --strip-component 1 

ENV SPARK_HOME=/opt/spark
ENV PATH=$PATH:$SPARK_HOME/bin:$SPARK_HOME/sbin
ENV PYSPARK_PYTHON=/usr/bin/python