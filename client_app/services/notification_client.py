import requests

class NotificationClient:
    BASE_URL = "http://localhost:5000"  
    def get_notifications(self, user_id):
        try:
            response = requests.get(f"{self.BASE_URL}/notifications/{user_id}")
            return response.json().get("notifications", [])
        except Exception as e:
            print("Error fetching notifications:", e)
            return []

    def get_notification_config(self, user_id):
        try:
            response = requests.get(f"{self.BASE_URL}/notifications/config/{user_id}")
            return response.json().get("configurations", [])
        except Exception as e:
            print("Error fetching config:", e)
            return []

    def update_notification_status(self, user_id, config_id, is_enabled):
        try:
            payload = {"is_enabled": is_enabled}
            requests.patch(f"{self.BASE_URL}/notifications/config/{user_id}/{config_id}", json=payload)
        except Exception as e:
            print("Error updating config:", e)

    def set_keywords(self, user_id, keywords):
        try:
            payload = {"keywords": keywords}
            requests.post(f"{self.BASE_URL}/notifications/keywords/{user_id}", json=payload)
        except Exception as e:
            print("Error updating keywords:", e)
