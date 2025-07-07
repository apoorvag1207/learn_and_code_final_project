import requests
from utils.session import SessionManager

from main import NewsAggregatorClientApp


class NotificationConfigMenu:
    def __init__(self, user_data):
        self.user = user_data
        self.keywords = []
        self.keywords_enabled = False

    def configure(self):
        while True:
            try:
                self.fetch_config()  

                print("\nC O N F I G U R E - N O T I F I C A T I O N S")
                for index, item in enumerate(self.config, 1):
                    status = "Enabled" if item["is_enabled"] else "Disabled"
                    print(f"{index}. {item['category'].capitalize()} - {status}")

                print(f"{len(self.config)+1}. Keywords - {'Enabled' if self.keywords_enabled else 'Disabled'}")
                print(f"{len(self.config)+2}. Back")
                print(f"{len(self.config)+3}. Logout")

                choice = input("Enter your option: ").strip()
                if choice.isdigit():
                    choice = int(choice)
                    if 1 <= choice <= len(self.config):
                        config_id = self.config[choice - 1]["id"]
                        self.toggle_category(config_id)
                    elif choice == len(self.config) + 1:
                        self.configure_keywords()
                    elif choice == len(self.config) + 2:
                        return
                    elif choice == len(self.config) + 3:
                        
                        NewsAggregatorClientApp().show_main_menu()
                        return
                    else:
                        print("Invalid option.")
                else:
                    print("Enter a valid number.")
            except Exception as e:
                print(f"Error loading configuration: {e}")

    def fetch_config(self):
        response = requests.get(f"http://localhost:5000/user/notification-config/{self.user['user_id']}")
        data = response.json()
        self.config = data.get("config", [])
        self.keywords = data.get("keywords", [])
        self.keywords_enabled = len(self.keywords) > 0

    def toggle_category(self, config_id):
        try:
            response = requests.patch(
                f"http://localhost:5000/user/notification-config/toggle/{self.user['user_id']}/{config_id}"
            )
            if response.status_code == 200:
                print("Category notification updated.")
            else:
                print("Update failed.")
        except Exception as e:
            print(f"Error: {e}")

    def configure_keywords(self):
        print("\nWould you like to update your keywords?")
        print("1. Yes")
        print("2. No (Go Back)")
        option = input("Choose an option: ").strip()

        if option == "1":
            new_keywords = input("Enter new keywords (comma-separated): ").strip()
            try:
                response = requests.post(
                    f"http://localhost:5000/user/keywords",
                    json={
                        "user_id": self.user["user_id"],
                        "keywords": [kw.strip() for kw in new_keywords.split(",") if kw.strip()]
                    }
                )
                if response.status_code == 200:
                    print("Keywords updated.")
                    self.fetch_config()  
                else:
                    print("Failed to update keywords.")
            except Exception as e:
                print(f"Error: {e}")
