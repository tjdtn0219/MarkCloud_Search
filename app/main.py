from fastapi import FastAPI
from app.api.search_controller import router as search_router
from app.core.elastic import close_es_client


app = FastAPI()
app.include_router(search_router, prefix="/api")


@app.on_event("shutdown")
async def shutdown_event():
    await close_es_client()
