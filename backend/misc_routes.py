from flask import Blueprint, g, jsonify, request

from auth import admin_required, login_required, worker_required
from db import call_proc, execute, fetch_all, fetch_one

bp = Blueprint("misc", __name__, url_prefix="/api")


# ---------- categories ----------

@bp.get("/categories")
def categories():
    return jsonify(fetch_all(
        "SELECT category_id, name, icon FROM categories ORDER BY name"))


# ---------- offers (accept / withdraw) ----------

@bp.put("/offers/<int:offer_id>/accept")
@login_required
def accept_offer(offer_id):
    row = fetch_one(
        "SELECT p.customer_id FROM offers o "
        "JOIN problems p ON p.problem_id = o.problem_id "
        "WHERE o.offer_id=%s", (offer_id,))
    if row is None:
        return jsonify({"error": "Offer not found"}), 404
    if row["customer_id"] != g.user["user_id"]:
        return jsonify({"error": "Only the problem owner can accept"}), 403
    # sp_accept_offer assigns the worker + rejects all other offers
    call_proc("sp_accept_offer", (offer_id,))
    return jsonify({"accepted": offer_id})


@bp.put("/offers/<int:offer_id>/withdraw")
@worker_required
def withdraw_offer(offer_id):
    offer = fetch_one("SELECT worker_id, status FROM offers WHERE offer_id=%s",
                      (offer_id,))
    if offer is None:
        return jsonify({"error": "Offer not found"}), 404
    if offer["worker_id"] != g.user["user_id"]:
        return jsonify({"error": "Not your offer"}), 403
    if offer["status"] != "pending":
        return jsonify({"error": "Only pending offers can be withdrawn"}), 400
    execute("UPDATE offers SET status='withdrawn' WHERE offer_id=%s",
            (offer_id,))
    return jsonify({"withdrawn": offer_id})


# ---------- messages ----------

@bp.get("/messages/conversations")
@login_required
def conversations():
    """One row per chat partner with the newest message."""
    uid = g.user["user_id"]
    return jsonify(fetch_all(
        "SELECT partner_id, CONCAT(u.first_name,' ',u.last_name) AS partner, "
        "       m.content AS last_message, m.sent_at, "
        "       (SELECT COUNT(*) FROM messages "
        "        WHERE sender_id = partner_id AND receiver_id = %s "
        "        AND is_read = FALSE) AS unread "
        "FROM ( "
        "  SELECT IF(sender_id=%s, receiver_id, sender_id) AS partner_id, "
        "         MAX(message_id) AS last_id "
        "  FROM messages WHERE sender_id=%s OR receiver_id=%s "
        "  GROUP BY partner_id "
        ") t "
        "JOIN messages m ON m.message_id = t.last_id "
        "JOIN users u ON u.user_id = t.partner_id "
        "ORDER BY m.sent_at DESC", (uid, uid, uid, uid)))


@bp.get("/messages/<int:partner_id>")
@login_required
def thread(partner_id):
    uid = g.user["user_id"]
    execute("UPDATE messages SET is_read=TRUE "
            "WHERE sender_id=%s AND receiver_id=%s", (partner_id, uid))
    return jsonify(fetch_all(
        "SELECT message_id, sender_id, content, problem_id, sent_at "
        "FROM messages WHERE (sender_id=%s AND receiver_id=%s) "
        "   OR (sender_id=%s AND receiver_id=%s) "
        "ORDER BY sent_at", (uid, partner_id, partner_id, uid)))


@bp.post("/messages/<int:partner_id>")
@login_required
def send_message(partner_id):
    d = request.get_json(silent=True) or {}
    content = (d.get("content") or "").strip()
    if not content:
        return jsonify({"error": "content required"}), 400
    if partner_id == g.user["user_id"]:
        return jsonify({"error": "Cannot message yourself"}), 400
    if not fetch_one("SELECT user_id FROM users WHERE user_id=%s "
                     "AND is_active=TRUE", (partner_id,)):
        return jsonify({"error": "User not found"}), 404
    msg_id = execute(
        "INSERT INTO messages (sender_id, receiver_id, content, problem_id) "
        "VALUES (%s,%s,%s,%s)",
        (g.user["user_id"], partner_id, content, d.get("problem_id")))
    execute("INSERT INTO notifications (user_id, type, message) "
            "VALUES (%s,'message',%s)",
            (partner_id, f"New message from {g.user['first_name']}"))
    return jsonify({"message_id": msg_id}), 201


# ---------- notifications ----------

@bp.get("/notifications")
@login_required
def notifications():
    unread_only = request.args.get("unread") == "1"
    sql = ("SELECT notification_id, type, message, is_read, created_at "
           "FROM notifications WHERE user_id=%s")
    if unread_only:
        sql += " AND is_read=FALSE"
    sql += " ORDER BY created_at DESC LIMIT 50"
    return jsonify(fetch_all(sql, (g.user["user_id"],)))


@bp.put("/notifications/read")
@login_required
def mark_read():
    ids = (request.get_json(silent=True) or {}).get("ids")
    if ids:
        placeholders = ",".join(["%s"] * len(ids))
        execute(f"UPDATE notifications SET is_read=TRUE WHERE user_id=%s "
                f"AND notification_id IN ({placeholders})",
                (g.user["user_id"], *ids))
    else:   # no ids -> mark everything read
        execute("UPDATE notifications SET is_read=TRUE WHERE user_id=%s",
                (g.user["user_id"],))
    return jsonify({"read": ids or "all"})


# ---------- admin ----------

@bp.get("/admin/stats")
@admin_required
def admin_stats():
    return jsonify({
        "category_demand":     fetch_all("SELECT * FROM v_category_demand"),
        "top_searches":        fetch_all("SELECT * FROM v_top_searches LIMIT 20"),
        "registration_growth": fetch_all("SELECT * FROM v_registration_growth"),
        "top_problems":        fetch_all("SELECT * FROM v_problem_statistics "
                                         "ORDER BY total_offers DESC LIMIT 20"),
        "top_workers":         fetch_all("SELECT * FROM v_worker_search "
                                         "ORDER BY avg_rating DESC LIMIT 20"),
    })


@bp.post("/admin/reviews/detect-fakes")
@admin_required
def detect_fakes():
    call_proc("sp_detect_fake_reviews", ())
    return jsonify(fetch_all(
        "SELECT review_id, worker_id, customer_id, flag_reason, created_at "
        "FROM reviews WHERE is_flagged=TRUE"))


@bp.put("/admin/users/<int:user_id>/deactivate")
@admin_required
def deactivate_user(user_id):
    execute("UPDATE users SET is_active=FALSE WHERE user_id=%s", (user_id,))
    return jsonify({"deactivated": user_id})


@bp.put("/admin/users/<int:user_id>/activate")
@admin_required
def activate_user(user_id):
    execute("UPDATE users SET is_active=TRUE WHERE user_id=%s", (user_id,))
    return jsonify({"activated": user_id})
