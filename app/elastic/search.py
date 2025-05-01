from .client import get_es_client


def search_product(keyword: str):
    es = get_es_client()
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                "fields": ["productName^2", "productNameEng", "applicationNumber"],
            }
        }
    }
    res = es.search(index="products", body=query)
    return res["hits"]["hits"]
