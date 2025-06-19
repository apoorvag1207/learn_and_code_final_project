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
            res = requests.get(url)
            return res.json() if res.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching articles: {e}")
            return []

    def save_article(self, user_id, article_id):
        try:
            url = f"{self.BASE_URL}/user/save"
            res = requests.post(url, json={"user_id": user_id, "article_id": article_id})
            return res.status_code == 200 and res.json().get("success", False)
        except Exception as e:
            print(f"Error saving article: {e}")
            return False
        
    def get_saved_articles(self, user_id):
        try:
            url = f"{self.BASE_URL}/user/saved?user_id={user_id}"
            res = requests.get(url)
            return res.json() if res.status_code == 200 else []
        except Exception as e:
            print(f"Error fetching saved articles: {e}")
            return []

    def delete_saved_article(self, user_id, article_id):
        try:
            url = f"{self.BASE_URL}/user/delete"
            res = requests.delete(url, json={"user_id": user_id, "article_id": article_id})
            return res.status_code == 200 and res.json().get("success", False)
        except Exception as e:
            print(f"Error deleting saved article: {e}")
            return False
        
    def search_articles(self, query):
        try:
            url = f"{self.BASE_URL}/user/search?query={query}"
            res = requests.get(url)
            return res.json() if res.status_code == 200 else []
        except Exception as e:
            print(f"Error searching articles: {e}")
            return []

