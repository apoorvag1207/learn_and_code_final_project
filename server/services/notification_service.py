from db_connection import DatabaseConnector
from utils.email_sender import EmailSender


class NotificationService:
    def __init__(self):
        self.db_connector = DatabaseConnector()
        self.email_sender = EmailSender()

    def get_notifications(self, user_id):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT 
                    Notification.Message,
                    Notification.SentAt,
                    NewsArticle.Title,
                    NewsArticle.URL
                FROM Notification
                JOIN NewsArticle ON Notification.NewsArticleId = NewsArticle.NewsArticleId
                WHERE Notification.UserId = %s
                ORDER BY Notification.SentAt DESC
                """,
                (user_id,),
            )
            return cursor.fetchall()
        except Exception as error:
            print(f"[ERROR] Fetching notifications: {error}")
            return []
        finally:
            cursor.close()
            connection.close()

    def get_notification_config(self, user_id):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT 
                    NotificationConfigId AS id, 
                    Category AS category, 
                    IsEnabled AS is_enabled
                FROM NotificationConfiguration
                WHERE UserId = %s
                """,
                (user_id,),
            )
            config_rows = cursor.fetchall()

            if not config_rows:
                print(f"No config found for user {user_id}, inserting defaults...")

                valid_categories = [
                    "Business", "Technology", "Sports", "Politics", "Health",
                    "Science", "Environment", "Entertainment"
                ]
                insert_query = """
                    INSERT INTO NotificationConfiguration (UserId, Category, IsEnabled, ReceiveEmails)
                    VALUES (%s, %s, 0, 1)
                """
                for category in valid_categories:
                    cursor.execute(insert_query, (user_id, category))
                connection.commit()

                cursor.execute(
                    """
                    SELECT 
                        NotificationConfigId AS id, 
                        Category AS category, 
                        IsEnabled AS is_enabled
                    FROM NotificationConfiguration
                    WHERE UserId = %s
                    """,
                    (user_id,),
                )
                config_rows = cursor.fetchall()
                print(f"Default config inserted for user {user_id}: {config_rows}")

            cursor.execute("SELECT Word FROM Keyword WHERE UserId = %s", (user_id,))
            keyword_rows = cursor.fetchall()
            keywords = [row["Word"] for row in keyword_rows]

            return {"config": config_rows, "keywords": keywords}

        except Exception as error:
            print(f"[ERROR] Failed to fetch or insert config: {error}")
            raise
        finally:
            cursor.close()
            connection.close()

    def update_notification_status(self, user_id, config_id, is_enabled):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                UPDATE NotificationConfiguration
                SET IsEnabled = %s
                WHERE NotificationConfigId = %s AND UserId = %s
                """,
                (1 if is_enabled else 0, config_id, user_id),
            )
            connection.commit()
        except Exception as error:
            print(f"[ERROR] Failed to update notification status: {error}")
            raise
        finally:
            cursor.close()
            connection.close()

    def set_keywords(self, user_id, keywords):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute("DELETE FROM Keyword WHERE UserId = %s", (user_id,))

            for word in keywords:
                cursor.execute(
                    "INSERT INTO Keyword (UserId, Word) VALUES (%s, %s)",
                    (user_id, word.strip()),
                )

            is_enabled = 1 if keywords else 0
            cursor.execute(
                """
                UPDATE NotificationConfiguration
                SET IsEnabled = %s
                WHERE UserId = %s AND Category = 'Keywords'
                """,
                (is_enabled, user_id),
            )

            connection.commit()
        except Exception as error:
            print(f"[ERROR] DB error in set_keywords: {error}")
            raise
        finally:
            cursor.close()
            connection.close()

    def notify_user(self, user_id, article_id, title, message):
        self.store_notification(user_id, article_id, message)
        self.send_email_notification(user_id, title, message)

    def store_notification(self, user_id, article_id, message):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO Notification (UserId, NewsArticleId, Message, SentAt, IsViewed)
                VALUES (%s, %s, %s, NOW(), 0)
                """,
                (user_id, article_id, message),
            )
            connection.commit()
            print(f"[INFO] Notification stored for user {user_id}")
        except Exception as error:
            print(f"[ERROR] Failed to store notification: {error}")
        finally:
            cursor.close()
            connection.close()

    def send_email_notification(self, user_id, title, message):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute("SELECT Email FROM User WHERE UserId = %s", (user_id,))
            row = cursor.fetchone()
            if row:
                subject = f"News Notification: {title}"
                self.email_sender.send_email(row["Email"], subject, message)
                print(f"[EMAIL SENT] To: {row['Email']}")
        except Exception as error:
            print(f"[ERROR] Failed to send email: {error}")
        finally:
            cursor.close()
            connection.close()

    def get_keywords(self, user_id):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT Word FROM Keyword WHERE UserId = %s", (user_id,))
        rows = cursor.fetchall()
        cursor.close()
        connection.close()
        return rows

    def get_users_to_notify(self, category, title):
        connection = self.db_connector.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                """
                SELECT DISTINCT UserId FROM NotificationConfiguration
                WHERE Category = %s AND IsEnabled = 1
                """,
                (category,),
            )
            category_users = set(row["UserId"] for row in cursor.fetchall())

            cursor.execute("SELECT DISTINCT UserId, Word FROM Keyword")
            keyword_rows = cursor.fetchall()
            keyword_users = {
                row["UserId"]
                for row in keyword_rows
                if row["Word"].lower() in title.lower()
            }

            return list(category_users.union(keyword_users))
        finally:
            cursor.close()
            connection.close()
