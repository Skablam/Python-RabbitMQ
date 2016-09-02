from kombu.mixins import ConsumerMixin
from kombu.log import get_logger
from kombu import Exchange, Queue
import uuid

exchange = Exchange('topic-test', type='topic')

# Create a queue for this consumer and give it a uuid for the name
queue = Queue(name=str(uuid.uuid4()), exclusive=True, exchange=exchange, routing_key='#')

logger = get_logger(__name__)


class Worker(ConsumerMixin):

    def __init__(self, connection):
        self.connection = connection

    def get_consumers(self, Consumer, channel):
        return [Consumer(queues=[queue],
                         accept=['pickle', 'json'],
                         callbacks=[self.process_message])]

    def process_message(self, body, message):
        logger.info("The body is {}".format(body))
        message.ack()

if __name__ == '__main__':
    from kombu import Connection
    from kombu.utils.debug import setup_logging
    # setup root logger
    setup_logging(loglevel='INFO', loggers=[''])

    with Connection('amqp://guest:guest@localhost:5672//', heartbeat=4) as conn:
        try:
            worker = Worker(conn)
            worker.run()
        except KeyboardInterrupt:
            print('bye bye')
