from fastapi import APIRouter
from app.models.search_schema import SearchRequest, PaginatedSearchResponse
from app.service.search_service import SearchService


router = APIRouter()
service = SearchService()


@router.post("/search", response_model=PaginatedSearchResponse)
async def search(req: SearchRequest):
    return await service.search(req)
