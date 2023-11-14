FROM ubuntu:20.04

RUN apt-get update \
    && apt-get install -y tzdata && ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime \
    && apt-get install -y git vim build-essential libssl-dev libffi-dev python-dev wget zip python3 python3-pip default-jdk scala

RUN wget https://archive.apache.org/dist/spark/spark-3.2.3/spark-3.2.3-bin-hadoop3.2.tgz