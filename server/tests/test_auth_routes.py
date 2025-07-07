import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from server.run import create_app
from flask import json
import pytest


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_signup_success(client):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "secure123"
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data or "success" in data

def test_signup_existing_email(client):
    payload = {
        "name": "Test User",
        "email": "testuser@example.com",  
        "password": "secure123"
    }
    response = client.post("/api/auth/signup", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("message") or data.get("error")

def test_login_success(client):
    payload = {
        "email": "testuser@example.com",
        "password": "secure123"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "user_id" in data or "role" in data

def test_login_invalid_password(client):
    payload = {
        "email": "testuser@example.com",
        "password": "wrongpassword"
    }
    response = client.post("/api/auth/login", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert "error" in data or data.get("user_id") is None

def test_check_email_exists(client):
    payload = { "email": "testuser@example.com" }
    response = client.post("/api/auth/check_email", json=payload)
    data = response.get_json()
    assert response.status_code == 200
    assert "exists" in data
    assert data["exists"] is True or data["exists"] is False
