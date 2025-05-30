import json
from elasticsearch import Elasticsearch, helpers
from dotenv import load_dotenv
import os

load_dotenv()

es = Elasticsearch(os.getenv("ES_HOST"))


INDEX_NAME = "products"


def recreate_index():
    if es.indices.exists(index=INDEX_NAME):
        es.indices.delete(index=INDEX_NAME)
        print(f"[INFO] 기존 인덱스 '{INDEX_NAME}' 삭제")

    index_settings = {
        "settings": {
            "analysis": {
                "analyzer": {
                    "ngram_analyzer": {
                        "type": "custom",
                        "tokenizer": "edge_ngram_tokenizer",
                        "filter": ["lowercase"],
                    }
                },
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 20,
                        "token_chars": ["letter", "digit", "whitespace"],
                    }
                },
            }
        },
        "mappings": {
            "properties": {
                "productName": {"type": "text", "analyzer": "ngram_analyzer"},
                "productNameEng": {"type": "text"},
                "applicationNumber": {"type": "keyword"},
                "applicationDate": {"type": "date", "format": "yyyyMMdd"},
                "registerStatus": {"type": "keyword"},
                "publicationNumber": {"type": "keyword"},
                "publicationDate": {"type": "date", "format": "yyyyMMdd"},
                "registrationNumber": {"type": "keyword"},
                "registrationDate": {"type": "date", "format": "yyyyMMdd"},
                "internationalRegNumbers": {"type": "keyword"},
                "internationalRegDate": {"type": "date", "format": "yyyyMMdd"},
                "priorityClaimNumList": {"type": "keyword"},
                "priorityClaimDateList": {"type": "date", "format": "yyyyMMdd"},
                "asignProductMainCodeList": {"type": "keyword"},
                "asignProductSubCodeList": {"type": "keyword"},
                "viennaCodeList": {"type": "keyword"},
            }
        },
    }

    es.indices.create(index=INDEX_NAME, body=index_settings)
    print(f"[SUCCESS] 인덱스 '{INDEX_NAME}' 생성 완료")


def bulk_insert_from_json(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    def flatten_dates(d):
        d["registrationNumber"] = d.get("registrationNumber", [None])
        d["registrationDate"] = d.get("registrationDate", [None])
        d["registrationNumber"] = (
            d["registrationNumber"][0] if d["registrationNumber"] else None
        )
        d["registrationDate"] = (
            d["registrationDate"][0] if d["registrationDate"] else None
        )
        return d

    actions = [{"_index": INDEX_NAME, "_source": flatten_dates(doc)} for doc in data]

    helpers.bulk(es, actions)
    print(f"[SUCCESS] {len(actions)}개 문서 업로드 완료")


if __name__ == "__main__":
    recreate_index()
    bulk_insert_from_json("data/trademarks.json")
