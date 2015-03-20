import kombu
import kombu.connection
import kombu.entity
import kombu.messaging

params = {
    'hostname': 'localhost',
    'port': 5672,
    'virtual_host': '/',
}

connection = kombu.connection.BrokerConnection(**params)
connection.connect()

exchange = kombu.entity.Exchange(name='kombu-test',
                                 type='topic',
                                 durable=False,
                                 auto_delete=False)

queue1 = kombu.Queue(name='queue1', exchange=exchange, routing_key='topic1')
queue1.maybe_bind(connection)
queue1.declare()

queue2 = kombu.Queue(name='queue2', exchange=exchange, routing_key='topic1')
queue2.maybe_bind(connection)
queue2.declare()

def process_message(body, message):
    print("The body is {}".format(body))
    print("The message is {}".format(message))
    message.ack()

consumer = kombu.Consumer(connection, queues=queue2, callbacks=[process_message], accept=[])
consumer.consume()

connection.drain_events(timeout=10)
