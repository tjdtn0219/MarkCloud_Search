from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import date


class SearchRequest(BaseModel):
    keyword: str = Field(..., description="검색 키워드")
    registerStatus: Optional[str] = Field(None, description="등록 상태 필터")
    asignProductMainCodeList: Optional[List[str]] = Field(
        None, description="상품 코드 필터"
    )
    registrationDateFrom: Optional[date] = Field(None, description="등록일 시작일")
    registrationDateTo: Optional[date] = Field(None, description="등록일 종료일")
    page: int = 1
    size: int = 10

class SearchResult(BaseModel):
    id: str
    score: float
    source: Dict[str, Any]

class PaginatedSearchResponse(BaseModel):
    total: int
    page: int
    size: int
    results: List[SearchResult]