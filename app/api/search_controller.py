from fastapi import APIRouter
from app.models.search_schema import SearchRequest
from app.service.search_service import SearchService

router = APIRouter()
service = SearchService()


@router.post("/search")
def search(req: SearchRequest):
    return service.search(req)
