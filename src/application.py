
import json

import pika

class Application:

    @staticmethod
    def create():
        return Application()

    def _prepare_worker(self, worker):
        def callback(channel, method_frame, header_frame, body):
            return worker(self, json.loads(body))
        return callback

    def connect_to_rabbitmq(self, connection_url):
        self.connection = pika.BlockingConnection(pika.URLParameters(connection_url))
        self.channel = self.connection.channel()

    def disconnect(self):
        self.channel.close()
        self.connection.close()

    def declare_exchange(self, exchange, exchange_type):
        self.channel.exchange_declare(exchange, exchange_type)
        
    def declare_queue(self, queue):
        self.channel.queue_declare(queue)

    def publish_message(self, queue, message):
        self.channel.basic_publish('', queue, json.dumps(message))

    def start_worker(self, queue, worker):
        self.channel.basic_consume(queue, self._prepare_worker(worker), auto_ack=True)
        self.channel.start_consuming()
        
    def stop_worker(self):
        self.channel.stop_consuming()
    