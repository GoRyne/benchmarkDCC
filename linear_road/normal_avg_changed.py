# -*- coding: utf-8 -*- 
import threading, logging, time, random
import os, sys
from multiprocessing import Process
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import csv
from datetime import datetime, timezone

## TODO) Need to clean up the dead process that end up with kill sig.

def producer(avgTuplesDuringInterval, timeInterval):
    producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
    topic = "test"
    print("Kafka producer started - Data ingestion to linear_road topic") 
    lastFilePosition = 0
    previousFileSize = 0
    currentFileSize = 0

    while True:
        previousFileSize = os.path.getsize("/data/datasets/output_0")

        if previousFileSize != currentFileSize:
            print("File size changed!")
            with open ("/data/datasets/output_0", "r") as myfile:

                currentFileSize = os.path.getsize("/data/datasets/output_0")
                myfile.seek(lastFilePosition)
                newContent = myfile.read()
                lastFilePosition = myfile.tell()
                newContent = newContent.split("\n")

                startTime = time.time()
                tmpCounter = 0
                randUniformNum = random.uniform(0, 1)

                if randUniformNum < (int(str(avgTuplesDuringInterval)[:2]) / 100):
                    randUniformNumTuples = random.randint(avgTuplesDuringInterval, pow(10, len(str(avgTuplesDuringInterval))))
                else:
                    randUniformNumTuples = random.randint(0, avgTuplesDuringInterval)
                
                for count, line in enumerate(newContent):

                    if tmpCounter == randUniformNumTuples:
                        # Generate new randUniformNum
                        randUniformNum = random.uniform(0, 1)
                        if randUniformNum < (int(str(avgTuplesDuringInterval)[:2]) / 100):
                            randUniformNumTuples = random.randint(avgTuplesDuringInterval, pow(10, len(str(avgTuplesDuringInterval))))
                        else:
                            randUniformNumTuples = random.randint(0, avgTuplesDuringInterval)
                        tmpCounter = 1
                        print(randUniformNum, randUniformNumTuples)
                    else:
                        tmpCounter += 1

                    producer.send(topic, line.encode('utf-8'))
                    
                    if randUniformNumTuples == 0:
                        print("randUniformNumTuples is zero; sleep for interval!")
                        time.sleep(timeInterval)
                        tmpCounter = 0
                        startTime = time.time() # Restart the timer.

                    if (randUniformNumTuples != 0) and (count % randUniformNumTuples == 0):
                        elapsedTime = time.time() - startTime
                        if elapsedTime < timeInterval:
                            time.sleep(timeInterval - elapsedTime)
                        else:
                            print("elpasedTime was bigger than " + str(timeInterval) + " sec!")
                        startTime = time.time() # Restart the timer.
        else:
            print("current File Size is still : " + str(currentFileSize))
            time.sleep(timeInterval)
            continue

def consumer(avgTuplesDuringInterval, timeInterval):
    topic = "test"
    consumer = KafkaConsumer(topic, bootstrap_servers=['localhost:9092'], 
                                enable_auto_commit=True, auto_offset_reset='latest',
                                max_poll_records=300000, max_partition_fetch_bytes=10485760)
    print("Kafka consumer started - Data copying from kafka topic to hdfs")

    while True:
        msg_dict = consumer.poll(max_records = pow(10, len(str(avgTuplesDuringInterval))))
        if len(msg_dict) == 0: # If there is no data from producer
            continue # Do not create data file
        
        data = []
        for key, messages in msg_dict.items():
            for msg in messages:
                timestamp = datetime.fromtimestamp((msg.timestamp / 1000), tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f") # 맨 마지막에 %Z 없어도 spark-rapids에서 GPU 함수 사용 가능
                row = str(msg.value)[2:-3] + "," + str(timestamp)
                data.append(list(row.split(',')))

        timestamp = time.time()
        filename = os.path.join("/data/datasets/inputcsv/" + str(timestamp) + ".csv")
        fp = open(filename, 'w', newline='')
        writer = csv.writer(fp)
        writer.writerows(data)
        fp.close()
        time.sleep(timeInterval) # control traffic


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Need argument (1): Average number of tuples during whole process")
        print("Need argument (2): Time Interval (sec)")
        sys.exit(1)
    else:
        avgTuplesDuringInterval = int(sys.argv[1])
        timeInterval = float(sys.argv[2])

    Process(target=producer, args=(avgTuplesDuringInterval, timeInterval,)).start()
    Process(target=consumer, args=(avgTuplesDuringInterval, timeInterval,)).start()
