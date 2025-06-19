import requests
from config import Config
from utils.validators import Validator

class SignUpHandler:
    def register_user(self):
        print("\n--- Sign Up ---")
        name = input("Enter username: ").strip()
        email = input("Enter email: ").strip()
        password = input("Enter password (min 6 characters): ").strip()

        if not Validator.is_valid_email(email):
            print("Invalid email format.")
            return

       
        if self.check_email_exists(email):
            print("Error: Email already registered. Please try a different email.\n")
            return

        if not Validator.is_valid_password(password):
            print("Password must be at least 6 characters.")
            return

        try:
            response = requests.post(
                f"{Config.BASE_URL}/api/auth/signup",
                json={"name": name, "email": email, "password": password}
            )
            print(response.json().get("message", "Signup response received."))
        except Exception as e:
            print(f"Error: {e}")

    def check_email_exists(self, email):
        try:
            response = requests.post(
                f"{Config.BASE_URL}/api/auth/check_email",  
                json={"email": email}
            )
            return response.json().get("exists", True)
        except Exception as e:
            print(f"[Client] Email check failed: {e}")
            return True
