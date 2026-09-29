import json

import requests

import common
import part2_store as store

MAX_RETRIES = 3
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2:1b"


def call_ai(text):
    resp = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": text, "stream": False},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["response"]


def on_message(ch, method, props, body):
    msg = json.loads(body)
    rid = msg["id"]
    retries = (props.headers or {}).get("retries", 0)

    try:
        answer = call_ai(msg["text"])
        store.put(rid, "completed", answer)
        ch.basic_ack(method.delivery_tag)
        print(f"id={rid} completed", flush=True)

    except Exception as e:
        print(f"id={rid} failed (retry {retries}): {e}", flush=True)
        if retries < MAX_RETRIES:
            ch.basic_publish(
                exchange="",
                routing_key="task_queue",
                body=body,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={"retries": retries + 1},
                ),
            )
            ch.basic_ack(method.delivery_tag)
        else:
            store.put(rid, "error", str(e))
            ch.basic_nack(method.delivery_tag, requeue=False)
            print(f"id={rid} sent to DLQ after {retries} retries", flush=True)


import pika  # needed for basic_publish properties above

conn = common.connect()
ch = conn.channel()
common.setup(ch)
ch.basic_qos(prefetch_count=1)
ch.basic_consume("task_queue", on_message)
print("consumer waiting for messages, Ctrl+C to stop", flush=True)
try:
    ch.start_consuming()
except KeyboardInterrupt:
    pass