
import unittest

import src.config

from src.application import Application


class TestApplication(unittest.TestCase):

    queue = 'test'
    messages = [ i for i in range(10) ]
    responses = []

    @property
    def expected_responses(self):
        return map(self.action, self.messages)

    @property
    def got_all_responses(self):
        return len(self.messages) == len(self.responses)

    @property
    def all_responses_matches(self):
        return all(r == e for r, e in zip(self.responses, self.expected_responses))

    def action(self, message):
        return message * 2

    def worker(self, application, message):
        self.responses.append(self.action(message))
        if self.got_all_responses:
            self.application.stop_worker()

    def make_assertions(self):
        self.assertTrue(self.got_all_responses)
        self.assertTrue(self.all_responses_matches)

    def start_application(self):
        self.application = Application()
        self.application.connect_to_rabbitmq(src.config.RABBITMQ_CONNECTION_URL)
        self.application.declare_queue(self.queue)
            
    def publish_messages(self):
        for message in self.messages:
            self.application.publish_message(self.queue, message)
    
    def wait_responses(self):
        self.application.start_worker(self.queue, self.worker)

    def close_application(self):
        self.application.disconnect()

    def test_application(self):
        self.start_application()
        self.publish_messages()
        self.wait_responses()
        self.make_assertions()
        self.close_application()
