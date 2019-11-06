from kafka import KafkaProducer
import os
import json


KAFKA_BROKER_URL = os.environ.get('KAFKA_BROKER_URL')
TASKS_TOPIC = os.environ.get('TASKS_TOPIC')
TASKS_PER_SECOND = float(os.environ.get('TASKS_PER_SECOND'))
SLEEP_TIME = 1 / TASKS_PER_SECOND


def send_content_service(task):
    """
    Producer sending tasks to kafka broker where the consumer should be the editor's platform
    :param task:
    :return:
    """
    producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER_URL,
        # Encode all values as JSON
        value_serializer = lambda value: json.dumps(value).encode())

    message = dict(task)
    producer.send(TASKS_TOPIC, value=message)
    return
