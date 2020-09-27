#!/usr/bin/python
# -*- coding: utf-8 -*-

import kafka
import os
from one_page_scraping import one_page_scraping


which_partition = os.environ.get('PARTITION')
which_topic = os.environ.get('TOPIC')

consumer = kafka.KafkaConsumer(
    bootstrap_servers=['172.105.202.99:9092'],
    auto_offset_reset='latest',
    enable_auto_commit=True,
    group_id='my-group',
    value_deserializer=lambda x: x.decode('utf-8'))

partition = kafka.TopicPartition(topic=which_topic, partition=int(which_partition))
consumer.assign([partition])

print(f'topicname : {which_topic}, partitions : {consumer.partitions_for_topic(which_topic)}')
print(f'target : {consumer.assignment()}')

print(f'Start consuming ...\n')

for record in consumer:
    message = record.value
    print(f'get message : ', message)
    try:
        url = message.split('|')[0]
        ts = message.split('|')[1]
        page = message.split('|')[2]
        one_page_scraping(url, ts, page)
    except IndexError:
        print('got wrong message . pass')

    
