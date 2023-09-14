import json
from datetime import datetime
from unittest.mock import patch

from app.constants import ES_TEST_INDEX


def test_create_entry(test_app_with_db):
    timestamp = datetime.now().isoformat()

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.post(
            "/entries/", data=json.dumps({"text": "hello", "timestamp": timestamp})
        )

    assert response.status_code == 201
    assert response.json()["text"] == "hello"
    assert response.json()["timestamp"] == timestamp


def test_create_entry_invalid_json(test_app):
    response = test_app.post("/entries/", data=json.dumps({}))
    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["body", "text"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }


def test_search_entry__search_by_text_single_result(test_app_with_db):
    text = "Stout"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries?query={text}")

    assert response.status_code == 200
    response_list = response.json()

    entry = response_list[0]
    assert entry.get("text") == "Kaedwenian Stout"
    assert entry.get("id") == "1"
    assert len(response_list) == 1


def test_search_entry__search_by_text_many_results(test_app_with_db):
    text = "Lager"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries?query={text}")

    assert response.status_code == 200
    response_list = response.json()

    assert len(response_list) == 2

    entry_0 = response_list[0]

    assert entry_0.get("text") == "Redanian Lager"
    assert entry_0.get("id") == "2"

    entry_1 = response_list[1]
    assert entry_1.get("text") == "Rivian Lager"
    assert entry_1.get("id") == "3"


def test_search_entry__search_by_text_many_results_fuzzy(test_app_with_db):
    text = "loger"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries?query={text}")

    assert response.status_code == 200
    response_list = response.json()

    assert len(response_list) == 2

    entry_0 = response_list[0]

    assert entry_0.get("text") == "Redanian Lager"
    assert entry_0.get("id") == "2"

    entry_1 = response_list[1]
    assert entry_1.get("text") == "Rivian Lager"
    assert entry_1.get("id") == "3"


def test_search_entry__search_by_timestamp_gte(test_app_with_db):
    start_date = "2023-09-12T00:00:00Z"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries?start_date={start_date}")

    assert response.status_code == 200
    response_list = response.json()

    entry = response_list[0]

    assert entry.get("text") == "Rivian Lager"
    assert entry.get("id") == "3"
    assert len(response_list) == 1


def test_search_entry__search_by_timestamp_lte(test_app_with_db):
    end_date = "2023-09-01T00:00:00Z"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries?end_date={end_date}")

    assert response.status_code == 200
    response_list = response.json()

    entry = response_list[0]

    assert entry.get("text") == "Kaedwenian Stout"
    assert entry.get("id") == "1"
    assert len(response_list) == 1


def test_search_entry__search_by_timestamp_range(test_app_with_db):
    start_date = "2023-09-01T00:00:00Z"
    end_date = "2023-09-06T00:00:00Z"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(
            f"/entries?start_date={start_date}&end_date={end_date}"
        )

    assert response.status_code == 200
    response_list = response.json()

    assert len(response_list) == 2

    entry_0 = response_list[0]

    assert entry_0.get("text") == "Kaedwenian Stout"
    assert entry_0.get("id") == "1"

    entry_1 = response_list[1]
    assert entry_1.get("text") == "Redanian Lager"
    assert entry_1.get("id") == "2"


def test_search_entry__empty_text_should_return_all(test_app_with_db):
    text = "Stout"

    with patch("app.api.crud.constants.ES_INDEX", ES_TEST_INDEX):
        response = test_app_with_db.get(f"/entries")

    assert response.status_code == 200
    response_list = response.json()

    assert len(response_list) == 3
