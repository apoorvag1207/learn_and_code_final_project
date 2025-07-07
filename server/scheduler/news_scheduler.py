from apscheduler.schedulers.background import BackgroundScheduler
from services.news_service import NewsService
from datetime import datetime, timedelta

class NewsScheduler:
    def __init__(self):
        self.scheduler = BackgroundScheduler()
        self.service = NewsService()

    def start(self):
        self.scheduler.add_job(self.service.fetch_and_store_all_news, 'interval', hours=4,next_run_time=datetime.now() + timedelta(hours=4) )
        # self.scheduler.add_job(
        #     self.service.fetch_and_store_all_news,
        #     'interval',
        #     seconds=220,  
        #     next_run_time=datetime.now()
        # )
        self.scheduler.start()
        print("Started news fetch scheduler.")
