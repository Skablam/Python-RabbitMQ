from kombu import Connection
import datetime

def add_message():
    with Connection('amqp://guest:guest@localhost:5672//') as conn:
        simple_queue = conn.SimpleQueue('simple_queue')
        message = 'helloword, sent at %s' % datetime.datetime.today()
        simple_queue.put(message)
        print('Sent: %s' % message)
        simple_queue.close()


add_message()
