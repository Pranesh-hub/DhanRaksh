from confluent_kafka import Producer
import json

conf = {
    "bootstrap.servers": "pkc-619z3.us-east1.gcp.confluent.cloud:9092",
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": "L4R6K2ZIQ7LZTVOR",
    "sasl.password": "cflt2g5VQQMORxUGuHt6U9VdJMI0bS/EUk4WrhBs5FZgDmt+znjI/7+rTfHEC6YA"
}

producer = Producer(conf)

def delivery_report(err, msg):
    if err is not None:
        print(f"Delivery failed: {err}")
    else:
        print(
            f"Delivered to {msg.topic()} "
            f"partition {msg.partition()}"
        )

def delivery_report(err, msg):
    if err:
        print("Delivery failed:", err)
    else:
        print(
            f"Delivered to {msg.topic()}"
        )

def publish_payment(event):

    producer.produce(
        "purchases",
        json.dumps(event)
    )

    producer.flush()