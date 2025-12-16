from flask import Blueprint, request, jsonify
from models import (
    get_feedbacks, add_feedback, delete_feedback,
    get_products,
    add_order, get_orders, update_order_status
)

api_bp = Blueprint("api", __name__)

# ----------------------------
# Helpers
# ----------------------------
def row_to_dict(row):
    # sqlite3.Row -> dict
    return dict(row) if row is not None else None


# ----------------------------
# PRODUCTS API (для форми замовлення)
# ----------------------------
@api_bp.route("/products", methods=["GET"])
def api_products_list():
    rows = get_products()
    data = [row_to_dict(r) for r in rows]
    return jsonify(data), 200


# ----------------------------
# FEEDBACK API
# ----------------------------
@api_bp.route("/feedbacks", methods=["GET"])
def api_feedbacks_list():
    rows = get_feedbacks()
    data = [row_to_dict(r) for r in rows]
    return jsonify(data), 200


@api_bp.route("/feedbacks", methods=["POST"])
def api_feedbacks_create():
    payload = request.get_json(silent=True) or {}

    name = (payload.get("name") or "Анонім").strip()
    message = (payload.get("message") or "").strip()

    if len(message) < 2:
        return jsonify({"error": "message must be at least 2 characters"}), 400

    add_feedback(name, message)
    return jsonify({"status": "success"}), 201


@api_bp.route("/feedbacks/<int:fid>", methods=["DELETE"])
def api_feedbacks_delete(fid):
    delete_feedback(fid)
    return jsonify({"status": "deleted"}), 200


# ----------------------------
# ORDERS API
# ----------------------------
@api_bp.route("/orders", methods=["GET"])
def api_orders_list():
    """
    Повертає список замовлень з товарами (як в адмінці).
    """
    orders = get_orders()
    out = []

    for odata in orders:
        order = row_to_dict(odata["order"])
        items = [row_to_dict(i) for i in odata["items"]]
        out.append({"order": order, "items": items})

    return jsonify(out), 200


@api_bp.route("/orders", methods=["POST"])
def api_orders_create():
    """
    Очікує JSON:
    {
      "customer_name": "Гість",
      "items": [{"product_id": 1, "quantity": 2}, ...]
    }
    """
    payload = request.get_json(silent=True) or {}
    customer_name = (payload.get("customer_name") or "Гість").strip()
    items = payload.get("items") or []

    if not isinstance(items, list) or len(items) == 0:
        return jsonify({"error": "items must be a non-empty list"}), 400

    normalized = []
    for it in items:
        try:
            pid = int(it.get("product_id"))
            qty = int(it.get("quantity", 1))
        except Exception:
            return jsonify({"error": "invalid items format"}), 400

        if pid <= 0 or qty <= 0:
            return jsonify({"error": "product_id and quantity must be positive"}), 400

        normalized.append((pid, qty))

    order_id = add_order(client_id=None, customer_name=customer_name, items=normalized)
    return jsonify({"status": "success", "order_id": order_id}), 201


@api_bp.route("/orders/<int:oid>", methods=["PATCH"])
def api_orders_update(oid):
    """
    Очікує JSON: { "status": "processing" }
    """
    payload = request.get_json(silent=True) or {}
    status = (payload.get("status") or "").strip()

    if len(status) < 2:
        return jsonify({"error": "status must be at least 2 characters"}), 400

    update_order_status(oid, status)
    return jsonify({"status": "updated"}), 200
