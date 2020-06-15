
import requests
import lorem

import src.config


class RankdoneService:

    @property
    def headers(self):
        return {
            'Authorization': f'Bearer {src.config.RANKDONE_TOKEN}'
        }

    def get_redactions(self, query):
        response = requests.get(src.config.RANKDONE_API, params=query, headers=self.headers)
        if response.status_code == 200:
            return response.json()
         

class RankdoneServiceMock(RankdoneService):

    RESULTS_PER_PAGE = 10
    MAX_PAGES = 100

    def generate_redactions(self, page):
        return [
            {
                'launch_id': (page - 1) * RankdoneServiceMock.RESULTS_PER_PAGE + i,
                'redaction': lorem.paragraph()
            } 
            for i in range(RankdoneServiceMock.RESULTS_PER_PAGE)
        ]

    def get_redactions(self, query):
        return {
            'step_id': query.get('step_id'),
            'page': query.get('page', 1),
            'max_pages': RankdoneServiceMock.MAX_PAGES, 
            'redactions': self.generate_redactions(query.get('page', 1))
        }