# from elasticsearch import Elasticsearch
from elasticsearch import AsyncElasticsearch
from typing import Optional
from dotenv import load_dotenv
import os

load_dotenv()

_es_client: Optional[AsyncElasticsearch] = None


async def get_es_client() -> AsyncElasticsearch:
    global _es_client
    if _es_client is None:
        _es_client = AsyncElasticsearch(hosts=[os.getenv("ES_HOST")])
        if not await _es_client.ping():
            raise ConnectionError("Elasticsearch 연결 실패")
    return _es_client


async def close_es_client():
    global _es_client
    if _es_client is not None:
        await _es_client.close()
