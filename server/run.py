from flask import Flask
from routes.auth_routes import auth_routes
from scheduler.news_scheduler import NewsScheduler
from routes.admin_routes import admin_routes
from routes.user_routes import user_routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_routes)
    app.register_blueprint(admin_routes)
    app.register_blueprint(user_routes)
    return app

if __name__ == "__main__":
    print("[System] Starting News Aggregator Backend API...")

    
    app = create_app()
    scheduler = NewsScheduler()
    
    scheduler.start()
    app.run(debug=True)

