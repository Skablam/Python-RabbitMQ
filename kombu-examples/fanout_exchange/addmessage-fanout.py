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

exchange = kombu.entity.Exchange(name='fanout-test',
                                 type='fanout')

producer = kombu.messaging.Producer(exchange=exchange,
                                    channel=channel,
                                    routing_key='who cares')

producer.publish('A message - {0}'.format(uuid.uuid4()))
