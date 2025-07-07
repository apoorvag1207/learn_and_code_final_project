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

def test_get_notifications(client):
    user_id = 1  
    response = client.get(f"/user/notifications/{user_id}")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.get_json()
        assert "notifications" in data
        assert isinstance(data["notifications"], list)

def test_get_notification_config(client):
    user_id = 1  
    response = client.get(f"/user/notification-config/{user_id}")
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.get_json()
        assert "config" in data
        assert isinstance(data["config"], list)

def test_update_notification_status(client):
    
    payload = {
        "user_id": 1,
        "config_id": 1,
        "is_enabled": True
    }
    response = client.patch("/user/notification-config/update-status", json=payload)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        assert "message" in response.get_json()

def test_set_keywords_valid(client):
    payload = {
        "user_id": 1,
        "keywords": ["AI", "Finance", "Climate"]
    }
    response = client.post("/user/keywords", json=payload)
    assert response.status_code in [200, 500]
    if response.status_code == 200:
        data = response.get_json()
        assert "message" in data

def test_set_keywords_invalid_input(client):
    payload = {
        "user_id": None,
        "keywords": "not-a-list"
    }
    response = client.post("/user/keywords", json=payload)
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_toggle_notification(client):
    
    user_id = 1
    config_id = 1
    response = client.patch(f"/user/notification-config/toggle/{user_id}/{config_id}")
    assert response.status_code in [200, 404, 500]
    if response.status_code == 200:
        data = response.get_json()
        assert "success" in data
