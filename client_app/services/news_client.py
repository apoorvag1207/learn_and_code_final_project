import requests

class NewsClient:
    BASE_URL = "http://localhost:5000"

    def fetch_headlines(self, date_input, category):
        try:
            if "|" in date_input:
                start, end = date_input.split("|")
                url = f"{self.BASE_URL}/user/headlines?start={start}&end={end}&category={category}"
            else:
                url = f"{self.BASE_URL}/user/headlines?date={date_input}&category={category}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching articles: {e}")
            return []

    def save_article(self, user_id, article_id):
        try:
            url = f"{self.BASE_URL}/user/save"
            response = requests.post(url, json={"user_id": user_id, "article_id": article_id})
            return response.status_code == 200 and response.json().get("success", False)
        except Exception as e:
            print(f"Error saving article: {e}")
            return False
        
    def get_saved_articles(self, user_id):
        try:
            url = f"{self.BASE_URL}/user/saved?user_id={user_id}"
            response = requests.get(url)
            return response.json() if response.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching saved articles: {e}")
            return []

    def delete_saved_article(self, user_id, article_id):
        try:
            url = f"{self.BASE_URL}/user/delete"
            response = requests.delete(url, json={"user_id": user_id, "article_id": article_id})
            return response.status_code == 200 and response.json().get("success", False)
        except Exception as e:
            print(f"Error deleting saved article: {e}")
            return False
        
 
    
    def search_articles(self, query, start_date=None, end_date=None):
        params = {"query": query}
        if start_date and end_date:
            params["start_date"] = start_date
            params["end_date"] = end_date

        try:
            url = f"{self.BASE_URL}/user/search"
            response = requests.get(url=url, params=params)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[ERROR] Search failed: {e}")
        return []

    def submit_feedback(self, user_id, article_id, is_liked):
        try:
            response = requests.post(
                f"{self.BASE_URL}/user/article/feedback",
                json={
                    "user_id": user_id,
                    "article_id": article_id,
                    "is_liked": is_liked
                }
            )
            return response.status_code == 200 and response.json().get("success")
        except Exception as error:
            print(f"[ERROR] Failed to submit feedback: {error}")
            return False

