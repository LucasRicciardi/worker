
class ApplicationError(Exception):
    pass

class QueueNotDeclaredError(ApplicationError):
    pass

class WorkerNotFoundError(ApplicationError):
    pass