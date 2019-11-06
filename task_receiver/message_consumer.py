from kafka import KafkaConsumer, KafkaProducer
import os
import json
import pandas as pd
import task_manager as task_manager

KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
DONE_TASKS_TOPIC = os.environ.get('DONE_TASKS_TOPIC')



if __name__ == "__main__":
    consumer = KafkaConsumer(
        DONE_TASKS_TOPIC,
        bootstrap_servers=KAFKA_BROKER_URL,
        value_deserializer=json.loads,
    )

    producer = KafkaProducer(
        bootstrap_servers=KAFKA_BROKER_URL,
        value_serializer=lambda value: json.dumps(value).encode(),
    )

    for message in consumer:
        task = pd.Series(dict(message.value))
        # task = pd.Series(task)
        task_manager.task_db_updater(task)
