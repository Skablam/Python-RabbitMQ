from kombu import Connection

def get_message():
    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        simple_queue = conn.SimpleQueue('simple_queue')
        message = simple_queue.get(block=True, timeout=1)
        print("Received: %s" % message.payload)
        message.ack()
        simple_queue.close()

get_message()
