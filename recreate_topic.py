import kafka  # kafka-python
import matplotlib  # for chinese file paths
import os
import time


def recreate():
    Admin = kafka.KafkaAdminClient(bootstrap_servers=['172.105.202.99:9092'])

    producer = kafka.KafkaProducer(bootstrap_servers=['172.105.202.99:9092'],
                                   value_serializer=lambda x: x.encode('utf-8'))

    partitions = int(os.environ.get('PARTITIONS'))
    which_topic = os.environ.get('TOPIC')

    print(producer.partitions_for('temp_data'))
    if len(producer.partitions_for('temp_data')) != partitions:
        Admin.delete_topics([which_topic])
        print(f'{which_topic} is deleted because wrong partitions')
        time.sleep(5)

        topic = kafka.admin.NewTopic(which_topic, partitions, 1)
        Admin.create_topics([topic])
        print(f'recreated')
