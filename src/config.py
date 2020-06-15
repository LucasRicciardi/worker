
import os

import dotenv


dotenv.load_dotenv()

ENV = os.getenv('ENV', 'dev')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'localhost')
RABBITMQ_PORT = os.getenv('RABBITMQ_PORT', '5672')
RABBITMQ_USERNAME = os.getenv('RABBITMQ_DEFAULT_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_DEFAULT_PASS', 'guest')
RABBITMQ_VIRTUAL_HOST = os.getenv('RABBITMQ_VIRTUAL_HOST', '')

RABBITMQ_CONNECTION_URL = 'amqp://{username}:{password}@{host}:{port}/{virtual_host}'.format(
    username=RABBITMQ_USERNAME,
    password=RABBITMQ_PASSWORD,
    host=RABBITMQ_HOST,
    port=RABBITMQ_PORT,
    virtual_host=RABBITMQ_VIRTUAL_HOST
)

APPLICATION_SRC_QUEUE = os.getenv('APPLICATION_SRC_QUEUE', 'worker_1_queue')
APPLICATION_DEST_QUEUE = os.getenv('APPLICATION_DEST_QUEUE', 'dest_queue')

WORKER_NAME = os.getenv('WORKER_NAME', 'worker_1')

WORKERS_DIR = 'src/workers'

RANKDONE_API = 'http://localhost:5000/redactions'
RANKDONE_TOKEN = ''