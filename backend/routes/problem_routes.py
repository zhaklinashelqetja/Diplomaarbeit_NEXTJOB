from flask import Blueprint, g, jsonify, request

from auth import login_required, optional_auth, worker_required
from db import call_proc, execute, fetch_all, fetch_one
from routes.user_routes import save_image

bp = Blueprint("problems", __name__, url_prefix="/api/problems")

def problem_card(extra_columns=""):
    """SQL for one problem "card" = what every problem list shows.
    Used here and in worker_routes (feed, saved problems), so the SQL
    exists only once. extra_columns adds columns, e.g. "r.score, "."""
    return (
        "SELECT " + extra_columns +
        "       p.problem_id, p.title, p.budget, p.urgency, p.status, "
        "       p.created_at, p.category_id, c.name AS category, "
        "       p.neighborhood_id, n.name AS neighborhood, "
        "       (SELECT COUNT(*) FROM offers o "
        "        WHERE o.problem_id = p.problem_id) AS offer_count, "
        "       (SELECT pp.file_path FROM problem_photos pp "
        "        WHERE pp.problem_id = p.problem_id "
        "        ORDER BY pp.sort_order LIMIT 1) AS cover_photo "
        "FROM problems p "
        "JOIN categories c    ON c.category_id     = p.category_id "
        "JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id ")


STATUSES = ("open", "assigned", "in_progress", "completed", "cancelled")


def owned_problem_or_404(problem_id):
    p = fetch_one("SELECT * FROM problems WHERE problem_id=%s", (problem_id,))
    if p is None:
        return None, (jsonify({"error": "Problem not found"}), 404)
    if p["customer_id"] != g.user["user_id"]:
        return None, (jsonify({"error": "Not your problem"}), 403)
    return p, None


@bp.get("")
@optional_auth
def list_problems():
    """Public problem browsing with filters. Also logs the search
    (search_logs) when a keyword or filter is used."""
    q            = request.args.get("q")
    category     = request.args.get("category", type=int)
    neighborhood = request.args.get("neighborhood", type=int)
    urgency      = request.args.get("urgency")
    status       = request.args.get("status", "open")
    page         = max(request.args.get("page", 1, type=int), 1)
    per_page     = min(request.args.get("per_page", 20, type=int), 50)

    sql, params = problem_card() + "WHERE 1=1", []
    if status in STATUSES:
        sql += " AND p.status=%s"; params.append(status)
    if q:
        sql += " AND (p.title LIKE %s OR p.description LIKE %s)"
        params += [f"%{q}%", f"%{q}%"]
    if category:
        sql += " AND p.category_id=%s"; params.append(category)
    if neighborhood:
        sql += " AND p.neighborhood_id=%s"; params.append(neighborhood)
    if urgency in ("low", "normal", "high", "emergency"):
        sql += " AND p.urgency=%s"; params.append(urgency)
    sql += " ORDER BY p.created_at DESC LIMIT %s OFFSET %s"
    params += [per_page, (page - 1) * per_page]
    rows = fetch_all(sql, tuple(params))

    if q or category or neighborhood:   # log the search for statistics
        execute("INSERT INTO search_logs (user_id, keyword, category_filter, "
                "neighborhood_filter) VALUES (%s,%s,%s,%s)",
                (g.user["user_id"] if g.user else None, q, category, neighborhood))
    return jsonify(rows)


@bp.get("/<int:problem_id>")
@optional_auth
def problem_detail(problem_id):
    p = fetch_one(
        "SELECT p.*, c.name AS category, n.name AS neighborhood, "
        "       CONCAT(u.first_name,' ',u.last_name) AS customer_name "
        "FROM problems p "
        "JOIN categories c    ON c.category_id     = p.category_id "
        "JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id "
        "JOIN users u         ON u.user_id         = p.customer_id "
        "WHERE p.problem_id=%s", (problem_id,))
    if p is None:
        return jsonify({"error": "Problem not found"}), 404
    # phone + street only for the customer and the worker who got the job
    me = g.user["user_id"] if g.user else None
    if me is None or me not in (p["customer_id"], p["assigned_worker_id"]):
        p.pop("contact_phone"); p.pop("address")
    p["photos"] = fetch_all(
        "SELECT file_path FROM problem_photos WHERE problem_id=%s "
        "ORDER BY sort_order", (problem_id,))
    execute("INSERT INTO problem_views (problem_id, user_id) VALUES (%s,%s)",
            (problem_id, me))   # view statistics
    return jsonify(p)


@bp.post("")
@login_required
def create_problem():
    d = request.get_json(silent=True) or {}
    required = ("category_id", "neighborhood_id", "title", "description",
                "contact_phone")
    if not all(d.get(k) for k in required):
        return jsonify({"error": f"Required: {', '.join(required)}"}), 400
    # unknown category/neighborhood, bad urgency or budget <= 0
    # are rejected by the database -> 400 (see app.py)
    problem_id = execute(
        "INSERT INTO problems (customer_id, category_id, neighborhood_id, "
        "address, title, description, contact_phone, budget, urgency, "
        "preferred_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (g.user["user_id"], d["category_id"], d["neighborhood_id"],
         d.get("address"), d["title"], d["description"], d["contact_phone"],
         d.get("budget"), d.get("urgency", "normal"), d.get("preferred_date")))
    return jsonify({"problem_id": problem_id}), 201


@bp.post("/<int:problem_id>/photos")
@login_required
def upload_photos(problem_id):
    _, err = owned_problem_or_404(problem_id)
    if err:
        return err
    files = request.files.getlist("photos")
    if not files:
        return jsonify({"error": "No files in field 'photos'"}), 400
    start = fetch_one("SELECT COUNT(*) AS n FROM problem_photos "
                      "WHERE problem_id=%s", (problem_id,))["n"]
    saved = []
    for i, f in enumerate(files):
        path = save_image(f, "problems")
        if path is None:
            return jsonify({"error": f"File {f.filename}: only "
                            "png/jpg/jpeg/webp allowed"}), 400
        execute("INSERT INTO problem_photos (problem_id, file_path, "
                "sort_order) VALUES (%s,%s,%s)", (problem_id, path, start + i))
        saved.append(path)
    return jsonify({"photos": saved}), 201


@bp.put("/<int:problem_id>")
@login_required
def update_problem(problem_id):
    p, err = owned_problem_or_404(problem_id)
    if err:
        return err
    if p["status"] != "open":
        return jsonify({"error": "Only open problems can be edited"}), 400
    d = request.get_json(silent=True) or {}
    allowed = ("title", "description", "category_id", "neighborhood_id",
               "address", "contact_phone", "budget", "urgency",
               "preferred_date")
    updates = {k: d[k] for k in allowed if k in d}
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400
    sets = ", ".join(f"{k}=%s" for k in updates)
    execute(f"UPDATE problems SET {sets} WHERE problem_id=%s",
            (*updates.values(), problem_id))
    return jsonify({"updated": list(updates)})


@bp.delete("/<int:problem_id>")
@login_required
def cancel_problem(problem_id):
    p, err = owned_problem_or_404(problem_id)
    if err:
        return err
    if p["status"] in ("completed", "cancelled"):
        return jsonify({"error": "Problem already finished"}), 400
    execute("UPDATE problems SET status='cancelled' WHERE problem_id=%s",
            (problem_id,))
    return jsonify({"cancelled": problem_id})


@bp.get("/mine")
@login_required
def my_problems():
    return jsonify(fetch_all(
        problem_card() + "WHERE p.customer_id=%s ORDER BY p.created_at DESC",
        (g.user["user_id"],)))


# ---------- offers on a problem ----------

@bp.get("/<int:problem_id>/offers")
@login_required
def list_offers(problem_id):
    _, err = owned_problem_or_404(problem_id)
    if err:
        return err
    return jsonify(fetch_all(
        "SELECT o.offer_id, o.price, o.message, o.status, o.initiated_by, "
        "       o.created_at, o.worker_id, ws.full_name AS worker, "
        "       ws.neighborhood, ws.avg_rating, ws.review_count, "
        "       ws.completed_jobs, ws.avg_response_hours "
        "FROM offers o "
        "JOIN v_worker_search ws ON ws.worker_id = o.worker_id "
        "WHERE o.problem_id=%s ORDER BY o.created_at", (problem_id,)))


@bp.post("/<int:problem_id>/offers")
@worker_required
def make_offer(problem_id):
    d = request.get_json(silent=True) or {}
    try:
        price = float(d.get("price"))
    except (TypeError, ValueError):
        price = 0
    if price <= 0:
        return jsonify({"error": "A positive price is required"}), 400
    # sp_make_offer enforces: problem open, not own problem, no duplicate
    call_proc("sp_make_offer",
              (g.user["user_id"], problem_id, price,
               d.get("message"), d.get("initiated_by", "worker")))
    offer = fetch_one("SELECT offer_id FROM offers WHERE problem_id=%s AND "
                      "worker_id=%s", (problem_id, g.user["user_id"]))
    return jsonify({"offer_id": offer["offer_id"]}), 201


# ---------- lifecycle ----------

@bp.put("/<int:problem_id>/start")
@login_required
def start_problem(problem_id):
    p = fetch_one("SELECT customer_id, assigned_worker_id, status "
                  "FROM problems WHERE problem_id=%s", (problem_id,))
    if p is None:
        return jsonify({"error": "Problem not found"}), 404
    if g.user["user_id"] not in (p["customer_id"], p["assigned_worker_id"]):
        return jsonify({"error": "Not involved in this job"}), 403
    if p["status"] != "assigned":
        return jsonify({"error": "Job is not in assigned state"}), 400
    execute("UPDATE problems SET status='in_progress' WHERE problem_id=%s",
            (problem_id,))
    return jsonify({"status": "in_progress"})


@bp.put("/<int:problem_id>/complete")
@login_required
def complete_problem(problem_id):
    _, err = owned_problem_or_404(problem_id)
    if err:
        return err
    call_proc("sp_complete_problem", (problem_id,))
    return jsonify({"status": "completed"})


@bp.post("/<int:problem_id>/review")
@login_required
def review_problem(problem_id):
    d = request.get_json(silent=True) or {}
    try:
        rating = int(d.get("rating"))
    except (TypeError, ValueError):
        rating = 0
    if not 1 <= rating <= 5:
        return jsonify({"error": "rating must be 1-5"}), 400
    # sp_leave_review enforces: completed, correct customer, no duplicate
    call_proc("sp_leave_review",
              (problem_id, g.user["user_id"], rating, d.get("text")))
    return jsonify({"reviewed": problem_id}), 201
