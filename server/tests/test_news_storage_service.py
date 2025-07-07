import pytest
from unittest.mock import MagicMock, patch
from services.news_storage_service import NewsStorageService
from datetime import datetime

@pytest.fixture
def sample_article():
    return {
        "title": "India launches new satellite",
        "description": "The satellite will monitor weather conditions.",
        "content": "article content goes here.",
        "url": "https://example.com/india-satellite",
        "publishedAt": "2025-07-01T10:30:00Z",
        "source": {"name": "SpaceNews"},
        "category": "Science"
    }

@pytest.fixture
def news_storage_service():
    service = NewsStorageService()
    service.db = MagicMock()
    service.category_inferer = MagicMock()
    service.notifier = MagicMock()
    return service

def test_parse_datetime_with_fraction(news_storage_service):
    datetime_str = "2025-07-01T10:30:00.000Z"
    result = news_storage_service.parse_datetime(datetime_str)
    assert result == datetime(2025, 7, 1, 16, 0)

def test_parse_datetime_without_fraction(news_storage_service):
    datetime_str = "2025-07-01T10:30:00Z"
    result = news_storage_service.parse_datetime(datetime_str)
    assert result == datetime(2025, 7, 1, 16, 0)

def test_extract_source_from_dict(news_storage_service):
    source = {"name": "BBC"}
    result = news_storage_service.extract_source(source)
    assert result == "BBC"

def test_extract_source_from_string(news_storage_service):
    result = news_storage_service.extract_source("Reuters")
    assert result == "Reuters"

def test_extract_source_fallback(news_storage_service):
    result = news_storage_service.extract_source(None)
    assert result == "Unknown"

@patch("services.news_storage_service.DatabaseConnector")
@patch("services.news_storage_service.NotificationService")
def test_save_article_inserts_and_notifies(mock_notification_class, mock_db_class, sample_article):
    mock_db_instance = mock_db_class.return_value
    mock_connection = MagicMock()
    mock_cursor = MagicMock()
    mock_connection.cursor.return_value = mock_cursor
    mock_db_instance.get_connection.return_value = mock_connection

    mock_cursor.fetchone.side_effect = [{"COUNT(*)": 0}, {"id": 123}]
    mock_notification_instance = mock_notification_class.return_value
    mock_notification_instance.get_users_to_notify.return_value = [1, 2]
    storage_service = NewsStorageService()
    storage_service.save_article(sample_article)

    
    assert mock_cursor.execute.call_count >= 3
    assert mock_notification_instance.notify_user.call_count == 2
    mock_cursor.close.assert_called_once()
    mock_connection.close.assert_called_once()

@patch("services.news_storage_service.NewsStorageService.save_article")
def test_bulk_store_articles_handles_each(mock_save_article):
    storage_service = NewsStorageService()
    articles = [{"title": "Title 1"}, {"title": "Title 2"}]
    storage_service.bulk_store_articles(articles)

    assert mock_save_article.call_count == 2
