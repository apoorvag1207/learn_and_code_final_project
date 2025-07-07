from db_connection import DatabaseConnector
from datetime import datetime

class AdminService:
    def __init__(self):
        self.db = DatabaseConnector()

    def list_external_servers_status(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ExternalId,Name, IsActive, LastAccessed FROM ExternalServer")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def list_external_servers_details(self):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ExternalId, Name, ApiKey FROM ExternalServer")
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results

    def update_server_api_key(self, server_id, new_key):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE ExternalServer SET ApiKey = %s WHERE ExternalId = %s",
            (new_key, server_id)
        )
        conn.commit()
        updated = cursor.rowcount
        cursor.close()
        conn.close()
        return updated > 0

    def add_category(self, category_name, created_by):
        conn = self.db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO AdminDefinedCategory (CategoryName, Created_By) VALUES (%s, %s)",
            (category_name, created_by)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return True
