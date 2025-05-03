from elasticsearch import Elasticsearch
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("ES_HOST"))


def get_es_client():
    if not es.ping():
        raise ConnectionError("Elasticsearch 연결 실패")
    return es
