import json
import os
import pathlib

import pytest
from elasticsearch import Elasticsearch
from starlette.testclient import TestClient

from app.config import Settings, get_settings
from app.constants import ES_TEST_INDEX
from app.main import create_application


def get_settings_override():
    return Settings(testing=1, es_hosts=os.environ.get("ES_HOSTS"))


@pytest.fixture(scope="module")
def test_app():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override
    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down


@pytest.fixture(scope="module")
def test_app_with_db():
    # set up
    app = create_application()
    app.dependency_overrides[get_settings] = get_settings_override

    es = Elasticsearch(hosts=get_settings_override().es_hosts)
    es.indices.create(
        index=ES_TEST_INDEX,
        body={
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
            },
        },
    )

    load_test_fixtures(es)

    with TestClient(app) as test_client:
        # testing
        yield test_client

    # tear down
    es.indices.delete(index=ES_TEST_INDEX)


def load_test_fixtures(es):
    fixture_path = pathlib.Path("tests/fixtures/test_entries.json")
    with open(fixture_path, "rt") as fixture_file:
        fixture_data = json.loads(fixture_file.read())
        for entry in fixture_data:
            fields = entry["fields"]
            es.create(
                index=ES_TEST_INDEX,
                id=fields["id"],
                body={
                    "text": fields["text"],
                    "timestamp": fields["timestamp"],
                },
                refresh=True,
            )
