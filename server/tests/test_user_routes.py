import pytest
import sys
import os
from flask import json


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from server.run import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_headlines_by_date(client):
    response = client.get("/user/headlines", query_string={
        "date": "2025-06-20",
        "category": "technology"
    })
    assert response.status_code in [200, 400]  
    if response.status_code == 200:
        data = response.get_json()
        assert isinstance(data, list)

def test_get_headlines_by_range(client):
    response = client.get("/user/headlines", query_string={
        "start": "2025-06-18",
        "end": "2025-06-22",
        "category": "sports"
    })
    assert response.status_code in [200, 400]
    if response.status_code == 200:
        data = response.get_json()
        assert isinstance(data, list)

def test_save_article_missing_data(client):
    response = client.post("/user/save", json={})
    assert response.status_code == 400
    assert response.get_json()["success"] is False

def test_save_article_success(client):
    payload = {
        "user_id": 1,         
        "article_id": 100
    }
    response = client.post("/user/save", json=payload)
    assert response.status_code == 200
    assert "success" in response.get_json()

def test_get_saved_articles(client):
    response = client.get("/user/saved", query_string={"user_id": 1})
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

def test_delete_saved_article_missing_data(client):
    response = client.delete("/user/delete", json={})
    assert response.status_code == 400
    assert response.get_json()["success"] is False

def test_delete_saved_article(client):
    payload = {
        "user_id": 1,
        "article_id": 100
    }
    response = client.delete("/user/delete", json=payload)
    assert response.status_code in [200, 500]
    assert "success" in response.get_json()

def test_search_articles(client):
    response = client.get("/user/search", query_string={
        "query": "india",
        "start_date": "2025-06-18",
        "end_date": "2025-06-22"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
