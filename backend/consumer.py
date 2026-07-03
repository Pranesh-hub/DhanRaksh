from confluent_kafka import Consumer
import json

conf = {
    "bootstrap.servers": "pkc-619z3.us-east1.gcp.confluent.cloud:9092",
    "security.protocol": "SASL_SSL",
    "sasl.mechanisms": "PLAIN",
    "sasl.username": "L4R6K2ZIQ7LZTVOR",
    "sasl.password": "cflt2g5VQQMORxUGuHt6U9VdJMI0bS/EUk4WrhBs5FZgDmt+znjI/7+rTfHEC6YA",

    "group.id": "payshield-group",

    "auto.offset.reset": "earliest"
}

consumer = Consumer(conf)

consumer.subscribe(["purchases"])

print("Listening for payments...")

while True:

    msg = consumer.poll(1.0)

    if msg is None:
        continue

    if msg.error():
        print(msg.error())
        continue

    event = json.loads(
        msg.value().decode("utf-8")
    )

    print(
        "\nReceived Event:"
    )

    print(event)