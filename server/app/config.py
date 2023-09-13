import logging
from functools import lru_cache
from fastapi import HTTPException
from elasticsearch import AsyncElasticsearch
from pydantic import AnyUrl, BaseSettings


log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: bool = bool(0)
    es_hosts: AnyUrl = None


@lru_cache()
def get_settings() -> BaseSettings:
    log.info("Loading config settings from the environment...")
    return Settings()


es_instance = None


def get_elasticsearch():
    global es_instance

    # If we haven't created the instance, we do it once
    if not es_instance:
        try:
            es_instance = AsyncElasticsearch(hosts=get_settings().es_hosts)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail="Elasticsearch connection error"
            )

    return es_instance
