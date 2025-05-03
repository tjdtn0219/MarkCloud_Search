from app.models.search_schema import SearchRequest
from app.repository.search_repository import SearchRepository


class SearchService:
    def __init__(self):
        self.repo = SearchRepository()

    def search(self, req: SearchRequest):
        raw_hits = self.repo.search(req)
        return raw_hits
