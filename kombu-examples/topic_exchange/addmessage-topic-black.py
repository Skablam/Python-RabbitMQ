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

exchange = kombu.entity.Exchange(name='topic-test',
                                 type='topic')

producer = kombu.messaging.Producer(exchange=exchange,
                                    channel=channel,
                                    routing_key='msg.black')

queue = kombu.Queue(name='queue-black', exchange=exchange, routing_key='*.black')
queue.maybe_bind(connection)
queue.declare()

queue = kombu.Queue(name='queue-red', exchange=exchange, routing_key='*.red')
queue.maybe_bind(connection)
queue.declare()

queue = kombu.Queue(name='queue-green', exchange=exchange, routing_key='*.green.*')
queue.maybe_bind(connection)
queue.declare()

queue = kombu.Queue(name='queue-allcolours', exchange=exchange, routing_key='msg.#')
queue.maybe_bind(connection)
queue.declare()

producer.publish('black - {0}'.format(uuid.uuid4()))
