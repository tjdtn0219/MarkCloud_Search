from app.models.search_schema import SearchRequest
from app.core.elastic import get_es_client


class SearchRepository:
    def __init__(self):
        self.index_name = "products"

    async def search(self, req: SearchRequest):
        es = await get_es_client()
        must_filters = self.build_must_filters(req)

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

        from_ = (req.page - 1) * req.size

        res = await es.search(
            index=self.index_name, body=query, from_=from_, size=req.size
        )

        return res

    def build_must_filters(self, req: SearchRequest) -> list[dict]:
        filters = []

        if req.registerStatus:
            filters.append({"term": {"registerStatus": req.registerStatus}})

        if req.asignProductMainCodeList:
            filters.append(
                {"terms": {"asignProductMainCodeList": req.asignProductMainCodeList}}
            )

        if req.registrationDateFrom or req.registrationDateTo:
            date_range = {}
            if req.registrationDateFrom:
                date_range["gte"] = req.registrationDateFrom
            if req.registrationDateTo:
                date_range["lte"] = req.registrationDateTo
            filters.append({"range": {"registrationDate": date_range}})

        return filters
