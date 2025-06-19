import requests

class NewsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_news(self):
        try:
            url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("articles", [])
        except Exception as e:
            print(f"[NewsAPI] Error: {e}")
            return []

class TheNewsAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_news(self):
        try:
            # url = f"https://api.thenewsapi.com/v1/news/top?api_token={self.api_key}&locale=us"
            url = f"https://api.thenewsapi.com/v1/news/all?api_token={self.api_key}&language=en&limit=10"
            response = requests.get(url)
            response.raise_for_status()
            return response.json().get("data", [])
        except Exception as e:
            print(f"[TheNewsAPI] Error: {e}")
            return []

class FirebaseAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_news(self):
        try:
            url = "https://us-central1-symbolic-gift-98004.cloudfunctions.net/newsapi"
            headers = {"api-key": self.api_key}
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get("articles", [])
        except Exception as e:
            print(f"[FirebaseAPI] Error: {e}")
            return []
