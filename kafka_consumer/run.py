import time
from kafka import KafkaConsumer

kafka_topic_name = 'TEST_FEAST'
kafka_config_kwargs = {
    "bootstrap_servers": [
        "kafka_broker:9092"
    ],
    # "api_version":(2,5,0),
}

for i in range(20):
    try:
        consumer = KafkaConsumer(kafka_topic_name, **kafka_config_kwargs)
        print("SUCCESS: instantiated Kafka consumer")
        break
    except Exception as e:
        print(
            f"Trying to instantiate consumer with config {kafka_config_kwargs} with error {e}"
        )
        time.sleep(10)
        pass

for msg in consumer:
    print(msg)
