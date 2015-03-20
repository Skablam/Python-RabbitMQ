from pyrabbit.api import Client

cl = Client('localhost:55672', 'guest', 'guest')

queue_count = cl.get_queue_depth('/','simple_queue')

print(queue_count)
