from confluent_kafka import Consumer
import json
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

consumer = Consumer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'billing_service',
})


if __name__ == "__main__":
    consumer.subscribe(['default'])
    print("start")
    while True:
        msg = consumer.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            print("Consumer error: {}".format(msg.error()))
            continue

        print("Received message: {}".format(msg.value()))

        order = json.loads(msg.value())

    consumer.close()
