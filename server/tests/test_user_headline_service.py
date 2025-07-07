import pytest
from services.user_headline_service import UserHeadlineService
from db_connection import DatabaseConnector

@pytest.fixture
def headline_service():
    return UserHeadlineService()

@pytest.fixture
def test_user_and_date_range():
    return {
        "user_id": 1,
        "start_date": "2025-06-18",
        "end_date": "2025-06-22",
        "specific_date": "2025-06-20",
        "category": "general",
        "invalid_category": "nonexistent"
    }

def test_get_articles_by_specific_date(headline_service, test_user_and_date_range):
    result = headline_service.get_articles_by_date(
        test_user_and_date_range["specific_date"],
        test_user_and_date_range["category"]
    )
    assert isinstance(result, list)
    for article in result:
        assert article["category"].lower() == test_user_and_date_range["category"]

def test_get_articles_by_date_range(headline_service, test_user_and_date_range):
    result = headline_service.get_articles_by_date_range(
        test_user_and_date_range["start_date"],
        test_user_and_date_range["end_date"],
        "all"
    )
    assert isinstance(result, list)
    for article in result:
        assert "title" in article and "published_at" in article  

def test_get_articles_by_date_invalid_category_returns_empty(headline_service, test_user_and_date_range):
    result = headline_service.get_articles_by_date(
        test_user_and_date_range["specific_date"],
        test_user_and_date_range["invalid_category"]
    )
    assert isinstance(result, list)
    assert len(result) == 0

def test_search_articles_without_date_range(headline_service):
    query = "trump"
    results = headline_service.search_articles(query)
    assert isinstance(results, list)
    for article in results:
        assert query.lower() in article["title"].lower() or query.lower() in article["description"].lower()

def test_search_articles_with_date_range(headline_service, test_user_and_date_range):
    query = "india"
    results = headline_service.search_articles(
        query,
        test_user_and_date_range["start_date"],
        test_user_and_date_range["end_date"]
    )
    assert isinstance(results, list)
    for article in results:
        assert "published_at" in article  

def test_get_saved_articles(headline_service, test_user_and_date_range):
    user_id = test_user_and_date_range["user_id"]
    result = headline_service.get_saved_articles(user_id)
    assert isinstance(result, list)
    for article in result:
        assert "title" in article and "url" in article

def test_delete_saved_article_success_or_fail(headline_service, test_user_and_date_range):
    user_id = test_user_and_date_range["user_id"]
    conn = DatabaseConnector().get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO SavedArticle (UserId, NewsArticleId) VALUES (%s, %s)", (user_id, 100))
    conn.commit()
    saved_article_id = cursor.lastrowid
    cursor.close()
    conn.close()
    result = headline_service.delete_saved_article(user_id, saved_article_id)
    assert result is True
