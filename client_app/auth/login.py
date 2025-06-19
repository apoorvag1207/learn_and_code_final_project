import requests
from config import Config

class LoginHandler:
    def authenticate_user(self):
        print("\n--- Login ---")
        email = input("Enter email: ").strip()
        password = input("Enter password: ").strip()

        try:
            response = requests.post(
                f"{Config.BASE_URL}/api/auth/login",
                json={"email": email, "password": password}
            )

            data = response.json()
            if response.status_code == 200 and data.get("success", False):
                print(data.get("message"))
                return {
                    "user_id": data.get("user_id"),
                    "role": data.get("role"),
                    "name": data.get("name")
                }
            else:
                print(data.get("message", "Invalid credentials."))
                return None 
        except Exception as e:
            print(f"Error: {e}")
            return None
