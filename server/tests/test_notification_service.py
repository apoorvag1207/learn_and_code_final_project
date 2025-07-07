import pytest
from services.notification_service import NotificationService
from db_connection import DatabaseConnector


@pytest.fixture
def notification_service():
    return NotificationService()


@pytest.fixture
def test_user():
    return {
        "user_id": 1,
        "article_id": 1,
        "config_id": 1,
        "category": "Technology",
        "title": "New AI Breakthrough in Robotics",
        "message": "Robots can  learn like humans"
    }


def test_get_notifications(notification_service, test_user):
    result = notification_service.get_notifications(test_user["user_id"])
    assert isinstance(result, list)


def test_get_notification_config_initializes_if_missing(notification_service, test_user):
    result = notification_service.get_notification_config(test_user["user_id"])
    assert "config" in result
    assert "keywords" in result
    assert isinstance(result["config"], list)


def test_update_notification_status(notification_service, test_user):
    try:
        notification_service.update_notification_status(
            test_user["user_id"], test_user["config_id"], True
        )
        assert True  
    except Exception:
        pytest.fail("Failed to update notification status")


def test_set_keywords(notification_service, test_user):
    new_keywords = ["machine learning", "space"]
    notification_service.set_keywords(test_user["user_id"], new_keywords)

    result = notification_service.get_keywords(test_user["user_id"])
    fetched = [keywords["Word"] for keywords in result]
    assert all(keyword in fetched for keyword in new_keywords)


def test_store_notification(notification_service, test_user):
    try:
        notification_service.store_notification(
            test_user["user_id"],
            test_user["article_id"],
            test_user["message"]
        )
        assert True
    except Exception:
        pytest.fail("Notification storage failed")


def test_send_email_notification(notification_service, test_user, mocker):
    mock_send = mocker.patch("utils.email_sender.EmailSender.send_email")

    notification_service.send_email_notification(
        test_user["user_id"],
        test_user["title"],
        test_user["message"]
    )

    mock_send.assert_called_once()
    args = mock_send.call_args[0]
    assert test_user["message"] in args[2]


def test_notify_user_combined(notification_service, test_user, mocker):
    mock_send = mocker.patch("utils.email_sender.EmailSender.send_email")
    notification_service.notify_user(
        test_user["user_id"],
        test_user["article_id"],
        test_user["title"],
        test_user["message"]
    )
    mock_send.assert_called_once()


def test_get_keywords(notification_service, test_user):
    result = notification_service.get_keywords(test_user["user_id"])
    assert isinstance(result, list)


def test_get_users_to_notify(notification_service, test_user):
    users = notification_service.get_users_to_notify(
        test_user["category"],
        test_user["title"]
    )
    assert isinstance(users, list)
