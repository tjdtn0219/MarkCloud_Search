from .client import get_es_client
from app.models.schema import SearchRequest


def search_product(keyword: str):
    print("keyword : ", keyword)
    es = get_es_client()
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": keyword,
                            "fields": [
                                "productName^2",
                                "productNameEng",
                                "applicationNumber",
                            ],
                            "type": "best_fields",
                        }
                    },
                    {
                        "fuzzy": {
                            "productName": {
                                "value": keyword,
                                "fuzziness": "AUTO",
                                "boost": 0.8,
                            }
                        }
                    },
                ]
            }
        }
    }
    res = es.search(index="products", body=query)
    return res["hits"]["hits"]


def search_product_advanced(req: SearchRequest):
    es = get_es_client()

    must_filters = []

    # 필터: 등록 상태
    if req.registerStatus:
        must_filters.append({"term": {"registerStatus": req.registerStatus}})

    # 필터: 상품 주 분류 코드 (OR 조건)
    if req.asignProductMainCodeList:
        must_filters.append(
            {"terms": {"asignProductMainCodeList": req.asignProductMainCodeList}}
        )

    # 필터: 등록일 범위
    if req.registrationDateFrom or req.registrationDateTo:
        date_range = {}
        if req.registrationDateFrom:
            date_range["gte"] = req.registrationDateFrom.strftime("%Y%m%d")
        if req.registrationDateTo:
            date_range["lte"] = req.registrationDateTo.strftime("%Y%m%d")
        must_filters.append({"range": {"registrationDate": date_range}})

    query = {
        "query": {
            "bool": {
                "must": must_filters,
                "should": [
                    {
                        "multi_match": {
                            "query": req.keyword,
                            "fields": [
                                "productName^2",
                                "productNameEng",
                                "applicationNumber",
                            ],
                            "type": "best_fields",
                        }
                    },
                    {
                        "fuzzy": {
                            "productName": {
                                "value": req.keyword,
                                "fuzziness": "AUTO",
                                "boost": 0.8,
                            }
                        }
                    },
                ],
                "minimum_should_match": 1,
            }
        }
    }

    res = es.search(index="products", body=query)
    return res["hits"]["hits"]
