from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu import Exchange, Queue, Connection
import uuid

conn = Connection('amqp://guest:guest@localhost:5672//', heartbeat=4)

exchange = Exchange('fanout-test', type='fanout')

# Create a queue for this consumer and give it a uuid for the name
queue = Queue(name=str(uuid.uuid4()), exchange=exchange, routing_key='doesnt matter what this is')
queue.maybe_bind(conn)
queue.declare()

logger = get_logger(__name__)


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection
        self.id = uuid.uuid4()
        logger.info(self.id)

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[queue],
                         accept=['pickle', 'json'],
                         callbacks=[self.process_message])]

    def process_message(self, body, message):
        logger.info(self.id)
        logger.info("The body is {}".format(body))
        message.ack()

if __name__ == '__main__':
    from kombu.utils.debug import setup_logging
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    try:
        worker = Worker(conn)
        worker.run()
    except KeyboardInterrupt:
        print('bye bye')
