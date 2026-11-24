from flask import Blueprint, jsonify

from db import fetch_all

bp = Blueprint("leaderboard", __name__, url_prefix="/api")


@bp.get("/leaderboard")
def leaderboard():
    """Top 20 workers and top 20 employers.
    Worker score   = 10 per completed job + total stars from reviews.
    Employer score = 10 per completed job they posted + 5 per review written."""
    workers = fetch_all(
        "SELECT ws.worker_id AS user_id, u.first_name, u.last_name, "
        "       u.avatar_path AS avatar_url, ws.neighborhood AS location, "
        "       ws.completed_jobs, ws.review_count, "
        "       COALESCE(ws.avg_rating, 0) AS rating, "
        "       CAST(ws.completed_jobs * 10 + ROUND(COALESCE(ws.avg_rating, 0) "
        "            * ws.review_count) AS SIGNED) AS score "
        "FROM v_worker_search ws "
        "JOIN users u ON u.user_id = ws.worker_id "
        "WHERE u.is_active = TRUE "
        "ORDER BY score DESC, rating DESC "
        "LIMIT 20")

    employers = fetch_all(
        "SELECT u.user_id, u.first_name, u.last_name, "
        "       u.avatar_path AS avatar_url, n.name AS location, "
        "       COUNT(DISTINCT p.problem_id) AS posted_jobs, "
        "       COUNT(DISTINCT CASE WHEN p.status = 'completed' "
        "             THEN p.problem_id END) AS completed_jobs, "
        "       COUNT(DISTINCT r.review_id) AS review_count, "
        "       COUNT(DISTINCT CASE WHEN p.status = 'completed' "
        "             THEN p.problem_id END) * 10 "
        "       + COUNT(DISTINCT r.review_id) * 5 AS score "
        "FROM users u "
        "LEFT JOIN neighborhoods n ON n.neighborhood_id = u.neighborhood_id "
        "LEFT JOIN problems p ON p.customer_id = u.user_id "
        "LEFT JOIN reviews r  ON r.customer_id = u.user_id "
        "WHERE u.account_type = 'jobgeber' "
        "  AND u.is_admin = FALSE AND u.is_active = TRUE "
        "GROUP BY u.user_id, u.first_name, u.last_name, "
        "         u.avatar_path, n.name "
        "ORDER BY score DESC, posted_jobs DESC "
        "LIMIT 20")

    return jsonify({"workers": workers, "employers": employers})
