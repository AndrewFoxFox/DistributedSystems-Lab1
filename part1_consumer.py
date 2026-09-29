import sys
import json
import time
import datetime

import common

delay = float(sys.argv[1]) if len(sys.argv) > 1 else 1.0 # default delay of 1 second if not provided
auto = len(sys.argv) > 2 and sys.argv[2] == "auto" # when auto

conn = common.connect()
ch = conn.channel()
common.setup(ch)
ch.basic_qos(prefetch_count=1)


def on_message(ch, method, props, body):
    m = json.loads(body)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    print(f"id={m['id']} text={m['text']} processed_at={now} " # Print ID, text, and processing timestamp
          f"redelivered={method.redelivered}", flush=True) # Print the redelivered flag
    # {"id": 1, "text": "Process this request", "timestamp": "2026-10-05T12:00:00Z"
    time.sleep(delay)
    if not auto:
        ch.basic_ack(method.delivery_tag)


ch.basic_consume("task_queue", on_message, auto_ack=auto)
print("waiting for messages, Ctrl+C to stop", flush=True)
try:
    ch.start_consuming()
except KeyboardInterrupt:
    pass