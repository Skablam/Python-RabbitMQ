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

exchange = kombu.entity.Exchange(name='direct-test',
                                 type='direct',
                                 durable=False,
                                 auto_delete=False)

queue1 = kombu.Queue(name='queue1', exchange=exchange, routing_key='black')
queue1.maybe_bind(connection)
queue1.declare()

def process_message(body, message):
    print("The body is {}".format(body))
    print("The message is {}".format(message))
    message.ack()

consumer = kombu.Consumer(connection, queues=queue1, callbacks=[process_message], accept=[])
consumer.consume()

connection.drain_events(timeout=10)
