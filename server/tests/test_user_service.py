import pytest
from services.user_service import UserService
from db_connection import DatabaseConnector

@pytest.fixture(scope="module")
def db_connection():
    return DatabaseConnector().get_connection()

@pytest.fixture
def user_service():
    return UserService()

@pytest.fixture
def test_user_and_article_ids():
    return {
        "user_id": 1,
        "article_id": 100
    }

def cleanup_saved_article(user_id, article_id):
    conn = DatabaseConnector().get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "DELETE FROM SavedArticle WHERE UserId = %s AND NewsArticleId = %s",
            (user_id, article_id)
        )
        conn.commit()
    finally:
        cursor.close()
        conn.close()


def test_save_article_successfully(user_service, test_user_and_article_ids):
    user_id = test_user_and_article_ids["user_id"]
    article_id = test_user_and_article_ids["article_id"]

    cleanup_saved_article(user_id, article_id)  
    result = user_service.save_article(user_id, article_id)

    assert result is True, "Expected to successfully save a new article for user."


def test_save_article_duplicate_should_fail(user_service, test_user_and_article_ids):
    user_id = test_user_and_article_ids["user_id"]
    article_id = test_user_and_article_ids["article_id"]
    user_service.save_article(user_id, article_id)
    result = user_service.save_article(user_id, article_id)
    assert result is False, "Expected to fail when saving an already saved article."


def test_save_article_with_invalid_user_or_article(user_service):
    invalid_user_id = -1
    invalid_article_id = -99

    result = user_service.save_article(invalid_user_id, invalid_article_id)

    assert result is False, "Expected to fail when using invalid user/article IDs."
