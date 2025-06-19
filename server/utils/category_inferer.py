class CategoryInferer:
    def __init__(self):
        self.keywords_map = {
            "science": ["nasa", "space", "planet", "experiment", "discovery", "research"],
            "technology": ["technology", "tech", "ai", "robot", "apple", "microsoft", "google", "cyber", "software"],
            "health": ["covid", "virus", "hospital", "fitness", "mental health", "diet", "vaccine", "health"],
            "business": ["market", "stocks", "inflation", "revenue", "startup", "budget", "economy", "finance"],
            "sports": ["football", "fifa", "tournament", "match", "cricket", "tennis", "goal", "olympics"],
            "entertainment": ["movie", "celebrity", "film", "tv", "music", "series", "actor", "drama"],
            "politics": ["election", "biden", "modi", "president", "minister", "congress", "government"],
            "environment": ["climate", "pollution", "wildlife", "global warming"],
            "travel": ["travel", "tourism", "destination", "trip", "hotel"],
            "food": ["recipe", "cuisine", "restaurant", "dish", "cook"],
            "general": []
        }

    def infer_category(self, title, description):
        text = f"{title or ''} {description or ''}".lower()
        for category, keywords in self.keywords_map.items():
            if any(keyword in text for keyword in keywords):
                return category
        return "general"
