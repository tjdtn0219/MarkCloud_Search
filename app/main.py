from fastapi import FastAPI, Query
from app.elastic.search import search_product, search_product_advanced
from app.models.schema import SearchRequest


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/search")
def search(keyword: str = Query(...)):
    results = search_product(keyword)
    return {"results": results}


@app.post("/search2")
def search_adv(req: SearchRequest):
    es_results = search_product_advanced(req)
    return es_results
