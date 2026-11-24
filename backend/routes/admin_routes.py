"""Admin management page (/admin/verwaltung): list users and problems,
block/unblock users, edit and cancel problems. Admin only."""
from flask import Blueprint, g, jsonify, request

from auth import admin_required
from db import execute, fetch_all, fetch_one
from translation_service import translate_text
from translations import localize_rows

bp = Blueprint("admin", __name__, url_prefix="/api/admin")

PROBLEM_STATUSES = ("open", "assigned", "in_progress", "completed", "cancelled")


# ---------- users ----------

@bp.get("/users")
@admin_required
def list_users():
    return jsonify(fetch_all(
        "SELECT u.user_id, u.first_name, u.last_name, u.email, u.phone, "
        "       u.account_type, u.is_admin, u.is_active, u.is_verified, "
        "       n.name AS location, u.created_at "
        "FROM users u "
        "LEFT JOIN neighborhoods n ON n.neighborhood_id = u.neighborhood_id "
        "ORDER BY u.created_at DESC"))


@bp.patch("/users/<int:user_id>/status")
@admin_required
def set_user_status(user_id):
    d = request.get_json(silent=True) or {}
    if not isinstance(d.get("is_active"), bool):
        return jsonify({"error": "is_active must be true or false"}), 400
    user = fetch_one("SELECT user_id, is_admin FROM users WHERE user_id=%s",
                     (user_id,))
    if user is None:
        return jsonify({"error": "User not found"}), 404
    if user["is_admin"] or user_id == g.user["user_id"]:
        return jsonify({"error": "Admins cannot be blocked"}), 400
    execute("UPDATE users SET is_active=%s WHERE user_id=%s",
            (d["is_active"], user_id))
    return jsonify({"user_id": user_id, "is_active": d["is_active"]})


# ---------- problems ----------

@bp.get("/problems")
@admin_required
def list_problems():
    rows = localize_rows(fetch_all(
        "SELECT p.problem_id, p.title, p.description, p.status, "
        "       p.budget, p.urgency, p.created_at, "
        "       c.name AS category, c.name_translations AS category_translations, "
        "       n.name AS location, "
        "       CONCAT(u.first_name, ' ', u.last_name) AS customer_name "
        "FROM problems p "
        "JOIN categories c ON c.category_id = p.category_id "
        "JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id "
        "JOIN users u ON u.user_id = p.customer_id "
        "ORDER BY p.created_at DESC"), ("category",))
    for row in rows:
        row["category_name"] = row["category_localized"]   # shown on the page
    return jsonify(rows)


@bp.put("/problems/<int:problem_id>")
@admin_required
def update_problem(problem_id):
    d = request.get_json(silent=True) or {}
    if not fetch_one("SELECT problem_id FROM problems WHERE problem_id=%s",
                     (problem_id,)):
        return jsonify({"error": "Problem not found"}), 404
    if "status" in d and d["status"] not in PROBLEM_STATUSES:
        return jsonify({"error": "status must be one of: "
                                 + ", ".join(PROBLEM_STATUSES)}), 400
    for field in ("title", "description"):
        if field in d and not (d[field] or "").strip():
            return jsonify({"error": f"{field} cannot be empty"}), 400

    values = {k: d[k] for k in ("title", "description", "status") if k in d}
    if not values:
        return jsonify({"error": "Nothing to update"}), 400
    for field in ("title", "description"):          # new text -> new translation
        if field in values:
            values[f"{field}_translations"] = translate_text(values[field])
    sets = ", ".join(f"{k}=%s" for k in values)
    execute(f"UPDATE problems SET {sets} WHERE problem_id=%s",
            (*values.values(), problem_id))
    return jsonify({"updated": [k for k in values if not k.endswith("_translations")]})


@bp.delete("/problems/<int:problem_id>")
@admin_required
def cancel_problem(problem_id):
    """Cancels instead of deleting: a real DELETE would also remove the
    offers, photos and reviews (ON DELETE CASCADE) and change ratings."""
    if not fetch_one("SELECT problem_id FROM problems WHERE problem_id=%s",
                     (problem_id,)):
        return jsonify({"error": "Problem not found"}), 404
    execute("UPDATE problems SET status='cancelled' WHERE problem_id=%s",
            (problem_id,))
    return jsonify({"cancelled": problem_id})
