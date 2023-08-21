from kafka import KafkaProducer
from json import dumps
import time
import json

producer = KafkaProducer(
    acks = 0,
    bootstrap_servers = [
        "spark-worker-01:9092","spark-worker-02:9092","spark-worker-03:9092"
    ],
    value_serializer = lambda x: dumps(x).encode('utf-8')
)

topic = 'tweet'
start = time.time()
for i in range(10):
    data = {'num': str(i)}
    producer.send(topic, value=data)
    producer.flush()
    time.sleep(2)
print('elapsed: ', time.time()-start)
