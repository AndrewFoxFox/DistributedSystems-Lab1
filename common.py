import pika

def connect():
    return pika.BlockingConnection(pika.ConnectionParameters("localhost"))      # Create a connection to the RabbitMQ server running on localhost

def setup(ch):
    ch.exchange_declare("dlx", exchange_type="direct", durable=True)            # Declare a dead letter exchange
    ch.queue_declare("task_queue_dlq", durable=True)                            # Declare a dead letter queue
    ch.queue_bind("task_queue_dlq", "dlx", routing_key="task_queue")            # Bind the dead letter queue to the dead letter exchange
    ch.queue_declare("task_queue", durable=True,                                # Declare the main queue with dead letter exchange and routing key
                     arguments={"x-dead-letter-exchange": "dlx",                # Set the dead letter exchange for the main queue
                                "x-dead-letter-routing-key": "task_queue"})     #  Set the dead letter routing key for the main queue