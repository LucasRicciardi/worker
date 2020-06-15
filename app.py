
import src.config
import src.errors

from src.application import Application
from src.worker import Worker


app = Application.create()

app.connect_to_rabbitmq(src.config.RABBITMQ_CONNECTION_URL)

app.declare_queue(src.config.APPLICATION_SRC_QUEUE)
app.declare_queue(src.config.APPLICATION_DEST_QUEUE)

worker = Worker.get(src.config.WORKER_NAME)

try:
    app.start_worker(src.config.APPLICATION_SRC_QUEUE, worker)
except src.errors.ApplicationError as err:
    app.stop_worker()
    
app.disconnect()

