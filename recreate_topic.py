import kafka  # kafka-python
import matplotlib  # for chinese file paths
import os
import time
from dotenv import load_dotenv
import os

load_dotenv()
kafka_host = os.getenv('KAFKA_HOST')
kafka_port = os.getenv('KAFKA_PORT')

def recreate():
    Admin = kafka.KafkaAdminClient(bootstrap_servers=[f'{kafka_host}:{kafka_port}'])

    producer = kafka.KafkaProducer(bootstrap_servers=[f'{kafka_host}:{kafka_port}'],
                                   value_serializer=lambda x: x.encode('utf-8'))

    partitions = int(os.environ.get('PARTITIONS'))
    which_topic = os.environ.get('TOPIC')

    print(producer.partitions_for(which_topic))
    if len(producer.partitions_for(which_topic)) != partitions:
        Admin.delete_topics([which_topic])
        print(f'{which_topic} is deleted because wrong partitions')
        time.sleep(5)

        topic = kafka.admin.NewTopic(which_topic, partitions, 1)
        Admin.create_topics([topic])
        print(f'recreated')
