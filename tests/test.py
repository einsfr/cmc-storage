import threading
from time import time, sleep
from kombu import Connection, Exchange, Queue, Consumer


exchange = Exchange('test', 'direct')
test_queue = Queue('test', exchange=exchange, routing_key='test')
queues = [test_queue, ]
connection_params = {
    'hostname': 'localhost',
    'userid': 'guest',
    'password': 'guest',
    'virtual_host': '/',
    'port': 5672,
    'transport': 'amqp'
}


class Worker(threading.Thread):

    def __init__(self, name, sleep_time):
        self._worker_name = name
        self._sleep_time = sleep_time
        super().__init__()

    def run(self):
        connection = Connection(**connection_params)
        channel = connection.channel()
        channel.basic_qos(prefetch_size=0, prefetch_count=1, a_global=True)
        while True:
            with Consumer(channel, queues, callbacks=[self.on_message]):
                connection.drain_events()

    def on_message(self, body, message):
        print('{}: WORKER {} RECEIVED MESSAGE: {}'.format(time(), self._worker_name, body))
        sleep(self._sleep_time)
        message.ack()


if __name__ == '__main__':

    try:
        worker1 = Worker('w1', 2)
        worker1.start()
        print('worker1 started')
        worker2 = Worker('w2', 3)
        worker2.start()
        print('worker2 started')
    except KeyboardInterrupt:
        print('exit')

    i = 0

    while True:
        with Connection(**connection_params) as conn:
            msg = {'id': i}
            producer = conn.Producer(serializer='json')
            producer.publish(msg, exchange=exchange, routing_key='test', declare=queues)
            print('{}: PUBLISHED MESSAGE: {}'.format(time(), msg))
        sleep(0.5)
        i += 1
