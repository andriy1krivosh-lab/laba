from flask import Blueprint, request, jsonify
from models import get_feedbacks, add_feedback, delete_feedback

api_feedback_bp = Blueprint('api_feedback', __name__)

# ------------------------------
# 1. GET /api/v1/feedback - всі відгуки
# ------------------------------
@api_feedback_bp.route('/', methods=['GET'])
def get_all_feedbacks():
    feedbacks = get_feedbacks()
    feedback_list = [{
        "id": f["id"],
        "name": f["name"],
        "message": f["message"],
        "created_at": f["created_at"]
    } for f in feedbacks]
    return jsonify(feedback_list), 200

# ------------------------------
# 2. POST /api/v1/feedback - додати новий відгук
# ------------------------------
@api_feedback_bp.route('/', methods=['POST'])
def create_feedback():
    data = request.get_json()
    name = data.get("name", "Анонім")
    message = data.get("message")
    if not message or not message.strip():
        return jsonify({"error": "Повідомлення не може бути пустим"}), 400
    add_feedback(name, message)
    return jsonify({"message": "Відгук додано"}), 201

# ------------------------------
# 3. GET /api/v1/feedback/<id> - конкретний відгук
# ------------------------------
@api_feedback_bp.route('/<int:fid>', methods=['GET'])
def get_feedback(fid):
    feedbacks = get_feedbacks()
    feedback = next((f for f in feedbacks if f["id"] == fid), None)
    if not feedback:
        return jsonify({"error": "Відгук не знайдено"}), 404
    return jsonify({
        "id": feedback["id"],
        "name": feedback["name"],
        "message": feedback["message"],
        "created_at": feedback["created_at"]
    }), 200

# ------------------------------
# 4. PUT /api/v1/feedback/<id> - оновити відгук
# ------------------------------
@api_feedback_bp.route('/<int:fid>', methods=['PUT'])
def update_feedback(fid):
    data = request.get_json()
    message = data.get("message")
    if not message or not message.strip():
        return jsonify({"error": "Повідомлення не може бути пустим"}), 400

    feedbacks = get_feedbacks()
    feedback = next((f for f in feedbacks if f["id"] == fid), None)
    if not feedback:
        return jsonify({"error": "Відгук не знайдено"}), 404

    # Видаляємо старий і додаємо новий з тим же id (sqlite не підтримує пряме оновлення id)
    delete_feedback(fid)
    add_feedback(feedback["name"], message)
    return jsonify({"message": "Відгук оновлено"}), 200

# ------------------------------
# 5. DELETE /api/v1/feedback/<id> - видалити відгук
# ------------------------------
@api_feedback_bp.route('/<int:fid>', methods=['DELETE'])
def remove_feedback(fid):
    feedbacks = get_feedbacks()
    feedback = next((f for f in feedbacks if f["id"] == fid), None)
    if not feedback:
        return jsonify({"error": "Відгук не знайдено"}), 404
    delete_feedback(fid)
    return jsonify({"message": "Відгук видалено"}), 200

# ------------------------------
# 6. GET /api/v1/feedback/docs - проста документація
# ------------------------------
@api_feedback_bp.route('/docs', methods=['GET'])
def api_docs():
    docs = {
        "GET /api/v1/feedback": "Повертає всі відгуки",
        "POST /api/v1/feedback": {"description": "Додає новий відгук", "body": {"name": "string", "message": "string"}},
        "GET /api/v1/feedback/<id>": "Повертає відгук по id",
        "PUT /api/v1/feedback/<id>": {"description": "Оновлює відгук", "body": {"message": "string"}},
        "DELETE /api/v1/feedback/<id>": "Видаляє відгук по id"
    }
    return jsonify(docs), 200
