from db_connection import DatabaseConnector
import hashlib

class AuthService:
    def __init__(self):
        self.db = DatabaseConnector()

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def register_user(self, name, email, password, role='User'):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            hashed_password = self.hash_password(password)
            query = """
                INSERT INTO User (Name, Email, Password, Role)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (name, email, hashed_password, role))
            conn.commit()
            return {"success": True, "message": "User registered successfully."}
        except Exception as e:
            return {"success": False, "message": str(e)}
        finally:
            cursor.close()
            conn.close()

    def login_user(self, email, password):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT UserId, Name, Password, Role FROM user WHERE Email=%s", (email,))
            result = cursor.fetchone()

            if not result:
                print("No user found with this email.")
                return {
                    "success": False,
                    "message": "Invalid credentials."
                }

           
            hashed_input_password = self.hash_password(password)
            if result[2] == hashed_input_password:
                return {
                    "success": True,
                    "message": "Login successful.",
                    "user_id": result[0],
                    "name": result[1],
                    "role": result[3]
                }
            else:
                return {
                    "success": False,
                    "message": "Invalid credentials."
                }
        except Exception as e:
            return {
                "success": False,
                "message": f"Server error: {e}"
            }
        finally:
            cursor.close()
            conn.close()
            
    def is_email_registered(self, email):
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            query = "SELECT COUNT(*) FROM User WHERE Email = %s"
            cursor.execute(query, (email,))
            count = cursor.fetchone()[0]
            return count > 0
        except Exception as e:
            print(f" Email check failed: {e}")
            return True  
        finally:
            cursor.close()
            conn.close()

    
