from flask import Blueprint, g, jsonify, request

from auth import login_required, worker_required
from db import call_proc, execute, fetch_all, fetch_one, replace_list
from routes.problem_routes import problem_card

bp = Blueprint("workers", __name__, url_prefix="/api/workers")

SORTABLE = {"avg_rating", "avg_job_price", "avg_response_hours",
            "completed_jobs", "years_experience"}


@bp.get("")
def search_workers():
    """Find workers by price / time / quality — powered by v_worker_search.
    ?neighborhood=<id> keeps only workers who take jobs there."""
    category     = request.args.get("category", type=int)
    neighborhood = request.args.get("neighborhood", type=int)
    sort         = request.args.get("sort", "avg_rating")
    order        = "ASC" if request.args.get("order") == "asc" else "DESC"
    page         = max(request.args.get("page", 1, type=int), 1)
    per_page     = min(request.args.get("per_page", 20, type=int), 50)
    if sort not in SORTABLE:
        sort = "avg_rating"

    sql, params = "SELECT * FROM v_worker_search WHERE 1=1", []
    if category:
        sql += (" AND worker_id IN (SELECT user_id FROM worker_categories "
                "WHERE category_id=%s)")
        params.append(category)
    if neighborhood:
        sql += (" AND worker_id IN (SELECT user_id FROM worker_service_areas "
                "WHERE neighborhood_id=%s)")
        params.append(neighborhood)
    sql += (f" ORDER BY {sort} IS NULL, {sort} {order} "
            f"LIMIT %s OFFSET %s")
    params += [per_page, (page - 1) * per_page]
    return jsonify(fetch_all(sql, tuple(params)))


@bp.get("/<int:worker_id>")
def worker_profile(worker_id):
    profile = fetch_one(
        "SELECT ws.*, wp.bio FROM v_worker_search ws "
        "JOIN worker_profiles wp ON wp.user_id = ws.worker_id "
        "WHERE ws.worker_id=%s", (worker_id,))
    if profile is None:
        return jsonify({"error": "Worker not found"}), 404
    profile["categories"] = fetch_all(
        "SELECT c.category_id, c.name FROM worker_categories wc "
        "JOIN categories c ON c.category_id = wc.category_id "
        "WHERE wc.user_id=%s ORDER BY c.name", (worker_id,))
    profile["service_areas"] = fetch_all(
        "SELECT n.neighborhood_id, n.name FROM worker_service_areas a "
        "JOIN neighborhoods n ON n.neighborhood_id = a.neighborhood_id "
        "WHERE a.user_id=%s ORDER BY n.name", (worker_id,))
    profile["reviews"] = fetch_all(
        "SELECT r.rating, r.review_text, r.created_at, "
        "       CONCAT(u.first_name,' ',LEFT(u.last_name,1),'.') AS customer "
        "FROM reviews r JOIN users u ON u.user_id = r.customer_id "
        "WHERE r.worker_id=%s AND r.is_flagged=FALSE "
        "ORDER BY r.created_at DESC LIMIT 20", (worker_id,))
    return jsonify(profile)


@bp.post("/me")
@login_required
def become_worker():
    """A jobgeber who also wants to work. (A jobnehmer already got his
    profile at registration.)"""
    if g.user["is_worker"]:
        return jsonify({"error": "Worker profile already exists"}), 409
    d = request.get_json(silent=True) or {}
    execute(
        "INSERT INTO worker_profiles (user_id, headline, bio, "
        "years_experience) VALUES (%s,%s,%s,%s)",
        (g.user["user_id"], d.get("headline"), d.get("bio"),
         d.get("years_experience", 0)))
    return jsonify({"worker_id": g.user["user_id"]}), 201


@bp.put("/me")
@worker_required
def update_worker():
    d = request.get_json(silent=True) or {}
    allowed = ("headline", "bio", "years_experience", "is_available")
    updates = {k: d[k] for k in allowed if k in d}
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400
    sets = ", ".join(f"{k}=%s" for k in updates)
    execute(f"UPDATE worker_profiles SET {sets} WHERE user_id=%s",
            (*updates.values(), g.user["user_id"]))
    return jsonify({"updated": list(updates)})


def _id_list(key):
    """Reads {"<key>": [1, 2, 3]} from the body -> sorted list without
    duplicates, or None if it is not a non-empty list of numbers."""
    ids = (request.get_json(silent=True) or {}).get(key)
    if not isinstance(ids, list) or not ids:
        return None
    try:
        return sorted({int(i) for i in ids})
    except (TypeError, ValueError):
        return None


@bp.put("/me/categories")
@worker_required
def set_categories():
    ids = _id_list("category_ids")
    if ids is None:
        return jsonify({"error": "category_ids must be a non-empty list"}), 400
    replace_list("DELETE FROM worker_categories WHERE user_id=%s",
                 "INSERT INTO worker_categories (user_id, category_id) "
                 "VALUES (%s,%s)", g.user["user_id"], ids)
    return jsonify({"category_ids": ids})


@bp.put("/me/areas")
@worker_required
def set_areas():
    """Which neighborhoods the worker takes jobs in (used by the feed)."""
    ids = _id_list("neighborhood_ids")
    if ids is None:
        return jsonify({"error": "neighborhood_ids must be a non-empty list"}), 400
    replace_list("DELETE FROM worker_service_areas WHERE user_id=%s",
                 "INSERT INTO worker_service_areas (user_id, neighborhood_id) "
                 "VALUES (%s,%s)", g.user["user_id"], ids)
    return jsonify({"neighborhood_ids": ids})


@bp.get("/me/feed")
@worker_required
def for_you_feed():
    """The For You page: refresh recommendations (SQL baseline now,
    the Python algorithm will overwrite the same table later),
    then return them as problem cards with their score."""
    call_proc("sp_generate_recommendations", (g.user["user_id"],))
    return jsonify(fetch_all(
        problem_card("r.score, ") +
        "JOIN recommendations r ON r.problem_id = p.problem_id "
        "WHERE r.worker_id=%s AND p.status='open' "
        "ORDER BY r.score DESC, p.created_at DESC", (g.user["user_id"],)))


@bp.get("/me/offers")
@worker_required
def my_offers():
    return jsonify(fetch_all(
        "SELECT o.offer_id, o.price, o.status, o.created_at, "
        "       p.problem_id, p.title, p.status AS problem_status, "
        "       n.name AS neighborhood "
        "FROM offers o JOIN problems p ON p.problem_id = o.problem_id "
        "JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id "
        "WHERE o.worker_id=%s ORDER BY o.created_at DESC",
        (g.user["user_id"],)))


@bp.get("/me/jobs")
@worker_required
def my_jobs():
    """Jobs assigned to me (accepted work) — with phone + address,
    because now I need them."""
    return jsonify(fetch_all(
        "SELECT p.problem_id, p.title, p.status, p.contact_phone, p.address, "
        "       n.name AS neighborhood, o.price "
        "FROM problems p "
        "JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id "
        "JOIN offers o ON o.problem_id = p.problem_id "
        "     AND o.worker_id = p.assigned_worker_id AND o.status='accepted' "
        "WHERE p.assigned_worker_id=%s "
        "ORDER BY p.updated_at DESC", (g.user["user_id"],)))


# ---------- saved problems (worker bookmarks) ----------

@bp.get("/me/saved-problems")
@worker_required
def list_saved_problems():
    return jsonify(fetch_all(
        problem_card("sp.saved_at, ") +
        "JOIN saved_problems sp ON sp.problem_id = p.problem_id "
        "WHERE sp.worker_id=%s ORDER BY sp.saved_at DESC",
        (g.user["user_id"],)))


@bp.post("/me/saved-problems/<int:problem_id>")
@worker_required
def save_problem(problem_id):
    if not fetch_one("SELECT problem_id FROM problems WHERE problem_id=%s",
                     (problem_id,)):
        return jsonify({"error": "Problem not found"}), 404
    execute("INSERT IGNORE INTO saved_problems (worker_id, problem_id) "
            "VALUES (%s,%s)", (g.user["user_id"], problem_id))
    return jsonify({"saved": problem_id}), 201


@bp.delete("/me/saved-problems/<int:problem_id>")
@worker_required
def unsave_problem(problem_id):
    execute("DELETE FROM saved_problems WHERE worker_id=%s AND problem_id=%s",
            (g.user["user_id"], problem_id))
    return jsonify({"removed": problem_id})
