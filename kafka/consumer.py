#!/usr/bin/env python
# encoding: utf-8
from kafka import KafkaConsumer
import setting
conf = setting.kafka_setting
consumer = KafkaConsumer(conf['topic_name'], bootstrap_servers = conf['bootstrap_servers'])
try:
    for msg in consumer:
        key = msg.key #因为接收到的数据时bytes类型，因此需要解码
        value = msg.value
        print("%s-%d-%d key=%s value=%s" % (msg.topic, msg.partition, msg.offset, key, value))
        time.sleep(2)
except BaseException  as e:
    print('succeed.',e)