import kombu.connection
import kombu.entity
import kombu.messaging
import uuid


params = {
    'hostname': 'localhost',
    'port': 5672,
    'virtual_host': '/',
}

connection = kombu.connection.BrokerConnection(**params)

connection.connect()

channel = connection.channel()

exchange = kombu.entity.Exchange(name='direct-test',
                                 type='direct')

producer = kombu.messaging.Producer(exchange=exchange,
                                    channel=channel,
                                    routing_key='black')

# These three queues have the same routing key as the producer
queue = kombu.Queue(name='queue1', exchange=exchange, routing_key='black')
queue.maybe_bind(connection)
queue.declare()

queue = kombu.Queue(name='queue2', exchange=exchange, routing_key='black')
queue.maybe_bind(connection)
queue.declare()

queue = kombu.Queue(name='queue3', exchange=exchange, routing_key='black')
queue.maybe_bind(connection)
queue.declare()

# Note this queue has a different routing_key and therefore the producer does
# not send messages to it
queue = kombu.Queue(name='queue4', exchange=exchange, routing_key='red')
queue.maybe_bind(connection)
queue.declare()

producer.publish('Foo {0}'.format(uuid.uuid4()))
