
import random
import unittest
import itertools
import threading

import src.config

from src.application import Application


class TestIntegration(unittest.TestCase):

    QUEUE = 'results_queue'

    WORKER_1_QUEUE = 'worker_1_queue'
    WORKER_2_QUEUE = 'worker_2_queue'
    WORKER_3_QUEUE = 'worker_3_queue'

    STEPS = random.randint(1, 6)
    LAUNCHES = random.randint(10, 20)

    def setUp(self):
        self.responses = list()

    @property
    def worker_queues(self):
        return (TestIntegration.WORKER_1_QUEUE, TestIntegration.WORKER_2_QUEUE, TestIntegration.WORKER_3_QUEUE)

    @property
    def all_queues(self):
        return itertools.chain(self.worker_queues, [ TestIntegration.QUEUE ])
    
    @property
    def messages(self):
        for i in range(TestIntegration.STEPS):
            for j in range(TestIntegration.LAUNCHES):
                yield {
                    'step_id': i,
                    'launch_id': j if j > 0 else None
                }

    @property
    def expected_responses(self):
        return TestIntegration.STEPS * (TestIntegration.LAUNCHES + 1) 

    @property
    def stop_condition(self):
        return len(self.responses) == self.expected_responses

    def start_application(self):
        self.app = Application()
        self.app.connect_to_rabbitmq(src.config.RABBITMQ_CONNECTION_URL)

    def publish_messages(self):
        for message in self.messages:
            if message.get('launch_id') is None:
                for queue in (TestIntegration.WORKER_2_QUEUE, TestIntegration.WORKER_3_QUEUE):
                    self.app.publish_message(queue, message)
            else:
                self.app.publish_message(TestIntegration.WORKER_1_QUEUE, message)

    def wait_responses(self):
        def worker(application, message):
            self.responses.append(message)
            if self.stop_condition:
                application.stop_worker()
        self.app.start_worker(TestIntegration.QUEUE, worker)

    def declare_queues(self):
        for queue in self.all_queues:
            self.app.declare_queue(queue)

    def make_assertions(self):
        for response in self.responses:
            self.assertIn('step_id', response)
            self.assertIn('worker', response)
            self.assertIn('data', response)
            
    def test_integration(self):
        self.start_application()
        self.declare_queues()
        self.publish_messages()
        self.wait_responses()
        self.make_assertions()
