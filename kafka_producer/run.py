from datetime import datetime, timedelta
import time
import json
import base64
import os
from random import uniform

from kafka import KafkaAdminClient, KafkaProducer
from kafka.admin import NewTopic

kafka_topic_name = 'TEST_FEAST'
kafka_config_kwargs = {
    "bootstrap_servers": [
        "kafka_broker:9092"
    ],
    # "api_version":(2,5,0),
}

for i in range(20):
    try:
        producer = KafkaProducer(**kafka_config_kwargs)
        admin = KafkaAdminClient(**kafka_config_kwargs)
        print("SUCCESS: instantiated Kafka admin and producer")
        break
    except Exception as e:
        print(
            f"Trying to instantiate admin and producer with bootstrap servers {kafka_config_kwargs['bootstrap_servers']} with error {e}"
        )
        time.sleep(10)
        pass


try:
    # Create Kafka topic
    topic = NewTopic(name=kafka_topic_name, num_partitions=3, replication_factor=1)
    admin.create_topics([topic])
    print(f"Topic {kafka_topic_name} created")
except Exception as e:
    print(str(e))
    pass

start = time.time()
date_zero = datetime(2020, 1, 1, 12, 00, 00)
iteration = 0

entities = [
    {
        'entity_no': entity_no,
        'title': ["Mr", "Mrs", "Ms", "Dr"][int(uniform(0, 4)//1)],
        'firstname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
        'surname': base64.b64encode(os.urandom(int(uniform(2, 20)//1))).decode('ascii'),
        # turns out that feast expects datetime panda fields to be timestamps
        'date_of_birth': int((date_zero - timedelta(days=uniform(18, 65)*365)).timestamp()),
        # 'date_of_birth': str(date_zero - timedelta(days=uniform(18, 65)*365)),
    }
    for entity_no in range(2000)
]

while True:

    event_date_time = date_zero + timedelta(days=365.25*iteration)
    for e in entities:
        entity = {**e}
        entity['sys_eff_to'] = event_date_time + timedelta(days=uniform(180, 365*5))
        entity['sys_eff_from'] = event_date_time

        for field in ["sys_eff_from", "sys_eff_to"]:
            # entity[field] = entity[field].strftime("%Y-%m-%d %H:%M:%S")
            # turns out that feast expects datetime panda fields to be timestamps
            entity[field] = int(entity[field].timestamp())
            # entity[field] = str(entity[field])
        producer.send(
            kafka_topic_name,
            json.dumps(
                # the flink push job directly pushes this payload,
                # and the feast push endpoint directly passes the payload
                # to the pandas.DataFrame constructor...
                {
                    data_field: [data_value]
                    for data_field, data_value in entity.items()
                }
            ).encode()
        )
        time.sleep(0.5)

    iteration += 1
    time.sleep(5)
