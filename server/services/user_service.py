from db_connection import DatabaseConnector

class UserService:
    def __init__(self):
        self.db = DatabaseConnector()

    def save_article(self, user_id, article_id):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        try:
            
            cursor.execute(
                "SELECT COUNT(*) FROM SavedArticle WHERE UserId = %s AND NewsArticleId = %s",
                (user_id, article_id)
            )
            if cursor.fetchone()[0] > 0:
                return False  

            
            cursor.execute(
                "INSERT INTO SavedArticle (UserId, NewsArticleId) VALUES (%s, %s)",
                (user_id, article_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"[UserService] Error saving article: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
