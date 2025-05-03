from app.models.search_schema import SearchRequest
from app.core.elastic import get_es_client


class SearchRepository:
    def __init__(self):
        self.es = get_es_client()
        self.index_name = "products"

    def search(self, req: SearchRequest):
        must_filters = []

        if req.registerStatus:
            must_filters.append({"term": {"registerStatus": req.registerStatus}})
        if req.asignProductMainCodeList:
            must_filters.append(
                {"terms": {"asignProductMainCodeList": req.asignProductMainCodeList}}
            )
        if req.registrationDateFrom or req.registrationDateTo:
            date_range = {}
            if req.registrationDateFrom:
                date_range["gte"] = req.registrationDateFrom
            if req.registrationDateTo:
                date_range["lte"] = req.registrationDateTo
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

        res = self.es.search(index=self.index_name, body=query)
        return res["hits"]["hits"]
