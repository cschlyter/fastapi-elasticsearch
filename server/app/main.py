import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import entries, health
from app.config import get_async_elasticsearch

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()

    origins = [
        "http://localhost:3000",
    ]

    application.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    application.include_router(health.router)
    application.include_router(entries.router, prefix="/entries", tags=["entries"])

    return application


app = create_application()


@app.on_event("startup")
async def startup_event():
    log.info("Starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
    es = get_async_elasticsearch()
    await es.close()
