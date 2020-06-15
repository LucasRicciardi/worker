
import abc
import importlib
import os

import requests

import src.config

from src.services.rankdone_service import RankdoneService, RankdoneServiceMock

class Worker:
    
    WORKERS_DIR = os.path.abspath(src.config.WORKERS_DIR)
    WORKERS_MODULE = src.config.WORKERS_DIR.replace('/', '.')
    
    AVAILABLE_WORKERS = map(lambda f: f.replace('.py', ''), filter(lambda f: not f.startswith('__'), os.listdir(WORKERS_DIR)))

    def __init__(self, name):
        self.name = name
        self.rankdone_service = RankdoneService() if src.config.ENV != 'test' else RankdoneServiceMock()

    def __call__(self, application, message):
        self.run(application, message)

    def action(self, redactions):
        return redactions

    def get_redactions(self, query):
        redactions = []
        while query:
            data = self.rankdone_service.get_redactions(query)
            page, max_pages = int(data.get('page')), int(data.get('max_pages'))
            if page < max_pages:
                query.update(page=page + 1)
            else:
                query = None
            redactions.extend(data.get('redactions'))            
        return redactions

    def run(self, application, message):
        redactions = self.get_redactions(message)
        results = {
            'worker': self.name,
            'step_id': message.get('step_id'),
            'data': self.action(redactions)
        }
        application.publish_message(src.config.APPLICATION_DEST_QUEUE, results) 
        
    @staticmethod
    def get(name, *args, **kwargs):
        workername = next(w for w in Worker.AVAILABLE_WORKERS if w == name)
        module = importlib.import_module(f'{Worker.WORKERS_MODULE}.{workername}')
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if issubclass(attr, Worker) and attr_name != Worker.__name__:
                return attr(name, *args, **kwargs)
