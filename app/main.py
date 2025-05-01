from fastapi import FastAPI, Query
from app.elastic.search import search_product


app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


@app.get("/search")
def search(keyword: str = Query(...)):
    results = search_product(keyword)
    return {"results": results}
