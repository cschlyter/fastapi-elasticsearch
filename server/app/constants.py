ES_INDEX = "entries-index"

ES_TEST_INDEX = "test-index"

ES_MAPPING = {
    "dynamic": "strict",
    "properties": {
        "text": {
            "type": "text",
            "analyzer": "english",
        },
        "timestamp": {
            "type": "text",
            "analyzer": "english",
        },
    },
}
