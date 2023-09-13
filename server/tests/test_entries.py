import json
from datetime import datetime


def test_create_entry(test_app_with_db):
    timestamp = datetime.now().isoformat()
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


def test_read_all_entries(test_app_with_db):
    response = test_app_with_db.post("/entries/", data=json.dumps({"text": "hello"}))
    entry_id = response.json()["id"]

    response = test_app_with_db.get("/entries/")
    assert response.status_code == 200

    response_list = response.json()
    assert len(list(filter(lambda d: d["id"] == entry_id, response_list))) == 1
