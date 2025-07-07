from flask import Blueprint, request, jsonify
from services.user_headline_service import UserHeadlineService
from services.user_service import UserService

user_routes = Blueprint('user_routes', __name__)
headline_service = UserHeadlineService()

@user_routes.route("/user/headlines", methods=["GET"])
def get_headlines():
    start = request.args.get("start")
    end = request.args.get("end")
    date = request.args.get("date")
    category = request.args.get("category", "all").lower()

    if date:
        articles = headline_service.get_articles_by_date(date, category)
    elif start and end:
        articles = headline_service.get_articles_by_date_range(start, end, category)
    else:
        return jsonify({"error": "Missing date or date range"}), 400

    return jsonify(articles), 200
user_service = UserService()

@user_routes.route("/user/save", methods=["POST"])
def save_article():
    data = request.get_json()
    user_id = data.get("user_id")
    article_id = data.get("article_id")

    if not user_id or not article_id:
        return jsonify({"success": False, "message": "Missing user_id or article_id"}), 400

    success = user_service.save_article(user_id, article_id)
    return jsonify({"success": success}), 200

@user_routes.route("/user/saved", methods=["GET"])
def get_saved_articles():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400
    return jsonify(headline_service.get_saved_articles(user_id)), 200

@user_routes.route("/user/delete", methods=["DELETE"])
def delete_saved_article():
    data = request.get_json()
    user_id = data.get("user_id")
    article_id = data.get("article_id")

    if not user_id or not article_id:
        return jsonify({"success": False, "message": "Missing user_id or article_id"}), 400

    success = headline_service.delete_saved_article(user_id, article_id)
    return jsonify({"success": success}), 200 if success else 500

@user_routes.route("/user/search", methods=["GET"])
def search_articles():
    query = request.args.get("query")
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    
    print(f" Received: query={query}, start_date={start_date}, end_date={end_date}")
    

    if not query:
        return jsonify({"error": "Missing search query"}), 400

    results = headline_service.search_articles(query, start_date, end_date)
    print(f" Result count: {len(results)}")
    return jsonify(results), 200

@user_routes.route("/user/article/feedback", methods=["POST"])
def give_article_feedback():
    data = request.get_json()
    user_id = data.get("user_id")
    article_id = data.get("article_id")
    is_liked = data.get("is_liked")

    service = UserHeadlineService()
    success = service.give_article_feedback(user_id, article_id, is_liked)
    return jsonify({"success": success})









