from datetime import datetime

class SessionManager:
    @staticmethod
    def get_today_date():
        return datetime.now().strftime("%Y-%m-%d")

    @staticmethod
    def get_formatted_date_time():
        now = datetime.now()
        return f"{now.strftime('%d-%b-%Y')}\nTime: {now.strftime('%I:%M%p')}"
