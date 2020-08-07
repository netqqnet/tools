#!/usr/bin/env python
# encoding: utf-8
import socket
import kafka as kf
import setting

conf = setting.kafka_setting

print(conf)


producer = kf.KafkaProducer(bootstrap_servers=conf['bootstrap_servers'])

partitions = producer.partitions_for(conf['topic_name'])
print('Topic下分区: %s' % partitions)

try:
    future = producer.send(conf['topic_name'], 'hello kafka2!'.encode())
    future.get()
    print('send message succeed.')
except BaseException  as e:
    print('send message succeed.',e)