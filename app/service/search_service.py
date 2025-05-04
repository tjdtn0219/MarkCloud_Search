from app.models.search_schema import SearchRequest, SearchResult, PaginatedSearchResponse
from app.repository.search_repository import SearchRepository


class SearchService:
    def __init__(self):
        self.repo = SearchRepository()

    def search(self, req: SearchRequest):
        es_response = self.repo.search(req)
        hits = es_response["hits"]["hits"]
        total = es_response["hits"]["total"]["value"]

        results = [
            SearchResult(
                id=hit["_id"],
                score=hit["_score"],
                source=hit["_source"]  # 그대로 넘김
            )
            for hit in hits
        ]

        return PaginatedSearchResponse(
            total=total,
            page=req.page,
            size=req.size,
            results=results
        )