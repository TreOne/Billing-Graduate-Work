from confluent_kafka import Producer
import json
import time

producer = Producer({
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'billing_service',
})

test_dict = {
    "test": "hello world"
}

while True:
    time.sleep(10)
    print("start")
    print(test_dict)
    producer.produce(
        'default',
        json.dumps(test_dict, ensure_ascii=True)
    )


producer.flush()
