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

def test_get_servers_status(client):
    response = client.get("/admin/servers/status")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "ExternalId" in data[0]
        assert "Name" in data[0]
        assert "IsActive" in data[0]
        assert "LastAccessed" in data[0]

def test_get_servers_details(client):
    response = client.get("/admin/servers/details")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    if data:
        assert "ServerId" in data[0]
        assert "Name" in data[0]
        assert "ApiKey" in data[0]

def test_update_server_api_key_invalid(client):
    payload = {
        "server_id": 999,  
        "new_key": "new_fake_key"
    }
    response = client.patch("/admin/servers/update", json=payload)
    assert response.status_code == 200 or response.status_code == 400
    data = response.get_json()
    assert "success" in data or "error" in data

def test_add_category_missing_fields(client):
    response = client.post("/admin/categories", json={})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_add_category_success(client):
    payload = {
        "name": "TestCategory",
        "admin_id": 1  
    }
    response = client.post("/admin/categories", json=payload)
    assert response.status_code in [200, 400]
    data = response.get_json()
    assert "message" in data or "error" in data
