import json
import datetime

import pika

import common

conn = common.connect()
ch = conn.channel()
common.setup(ch)

for i in range(1, 11):
    msg = {
        "id": i,
        "text": "Process this request",
        "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    ch.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps(msg),
        properties=pika.BasicProperties(delivery_mode=2),
    )
    print("sent", i)

conn.close()