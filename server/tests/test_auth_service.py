import pytest
from services.auth_service import AuthService

@pytest.fixture
def service():
    return AuthService()

def test_register_user_success(service):
    conn = service.db.get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM User WHERE Email = %s", ("tester@example.com",))
    conn.commit()
    cursor.close()
    conn.close()

    response = service.register_user("Tester", "tester@example.com", "password123", "User")
    assert response["success"] is True


def test_register_user_duplicate(service):
    
    response = service.register_user("Tester", "tester@example.com", "password123", "User")
    assert response["success"] is False
    assert "Duplicate" in response["message"] or "already" in response["message"]

def test_login_user_success(service):
    response = service.login_user("tester@example.com", "password123")
    assert response["success"] is True
    assert "user_id" in response
    assert "name" in response

def test_login_user_wrong_password(service):
    response = service.login_user("tester@example.com", "wrongpass")
    assert response["success"] is False
    assert "Invalid credentials" in response["message"]

def test_login_user_nonexistent(service):
    response = service.login_user("nonexistent@example.com", "any")
    assert response["success"] is False
    assert "Invalid credentials" in response["message"]

def test_check_email_exists(service):
    exists = service.is_email_registered("tester@example.com")
    assert exists is True

def test_check_email_not_exists(service):
    exists = service.is_email_registered("unique_email_987@example.com")
    assert exists is False
