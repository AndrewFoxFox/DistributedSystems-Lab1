import json
import uuid

import pika
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import common
import part2_store as store

app = FastAPI()


class Req(BaseModel):
    text: str


@app.post("/process")
def process(req: Req):
    rid = str(uuid.uuid4())
    store.put(rid, "processing")
    conn = common.connect()
    ch = conn.channel()
    common.setup(ch)
    ch.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps({"id": rid, "text": req.text}),
        properties=pika.BasicProperties(delivery_mode=2, headers={"retries": 0}),
    )
    conn.close()
    return {"id": rid}


@app.get("/result/{rid}")
def result(rid: str):
    r = store.get(rid)
    if r is None:
        raise HTTPException(status_code=404, detail="unknown id")
    return {"id": rid, **r}