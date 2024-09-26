import pytest
from mongo_helpers.CRUD.insert_document import insert_document
from mongo_helpers.client.get_mongo_client import get_mongo_client


def test_insert_document():
    client, db = get_mongo_client()
    collection = db["test_collection"]
    document = {"name": "Test", "email": "test@example.com"}
    inserted_id = insert_document(collection, document)

    assert inserted_id is not None
    client.close()
