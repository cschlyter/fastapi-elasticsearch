import logging

from fastapi import FastAPI
from app.api import health, entries

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()

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
    await es.close()
