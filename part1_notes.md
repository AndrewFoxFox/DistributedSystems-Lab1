# Lab 1 Part 1 notes

## 1.3a: Manual ack

Killed consumer mid-message, so the message went back to the queue (10 Ready).
Restart showed `redelivered=True`.
Ack only after processing gives at-least-once delivery. Duplicates are possible, so processing must be safe to repeat

## 1.3b: Auto-ack

Killed consumer after the first message. Queue showed 0 Ready and 0 Unacked, but only 1 message was processed.
Auto-ack marks messages done on delivery, so anything received but unprocessed is lost (at-most-once).

## 1.3c: Persistence

Restarted the broker and 10 messages survived.
Needs both `durable=True` on the queue and `delivery_mode=2` on the messages.