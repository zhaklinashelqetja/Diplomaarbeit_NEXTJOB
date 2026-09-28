"""Review analysis (Data-Science module) - /api/analysis/*

  POST /api/analysis/preview        analyze any text, nothing stored   (login)
  POST /api/analysis/reviews/<id>   analyze one stored review + save   (admin)
  GET  /api/analysis/reviews/<id>   stored analysis of one review      (login)
  GET  /api/analysis/workers/<id>   strengths / weaknesses + sentiment (public)
  POST /api/analysis/run            analyze every review without one   (admin)

The models live in ml/models/ and are loaded once per worker at startup.
"""
from flask import Blueprint, jsonify, request

from auth import admin_required, login_required
from db import fetch_all, fetch_one, get_db
from ml.analyzer import MODEL_VERSION, analyze_review

bp = Blueprint("analysis", __name__, url_prefix="/api/analysis")


# ------------------------------------------------------------ helpers

def analyze_and_store(review_id, text):
    """Analyze one review and save the result (one transaction).
    Re-running it replaces the previous result for that review."""
    result = analyze_review(text)
    conn = get_db()
    cur = conn.cursor(dictionary=True)
    try:
        cur.execute(
            "INSERT INTO review_analysis "
            "  (review_id, sentiment, sentiment_confidence, model_version) "
            "VALUES (%s, %s, %s, %s) AS new "
            "ON DUPLICATE KEY UPDATE sentiment = new.sentiment, "
            "  sentiment_confidence = new.sentiment_confidence, "
            "  model_version = new.model_version",
            (review_id, result["sentiment"], result["sentiment_confidence"],
             MODEL_VERSION))
        cur.execute("SELECT analysis_id FROM review_analysis "
                    "WHERE review_id = %s", (review_id,))
        analysis_id = cur.fetchone()["analysis_id"]
        cur.execute("DELETE FROM review_analysis_categories "
                    "WHERE analysis_id = %s", (analysis_id,))
        for c in result["categories"]:
            cur.execute(
                "INSERT INTO review_analysis_categories "
                "  (analysis_id, category, polarity, score) "
                "VALUES (%s, %s, %s, %s)",
                (analysis_id, c["category"], c["polarity"], c["score"]))
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()
    return result


def analyze_pending():
    """Analyze every review that has no analysis yet. Returns the count."""
    todo = fetch_all(
        "SELECT r.review_id, r.review_text FROM reviews r "
        "LEFT JOIN review_analysis ra ON ra.review_id = r.review_id "
        "WHERE ra.review_id IS NULL")
    for row in todo:
        analyze_and_store(row["review_id"], row["review_text"])
    return len(todo)


# ------------------------------------------------------------- routes

@bp.post("/preview")
@login_required
def preview():
    """Analyze arbitrary text without storing it - for the live demo."""
    text = (request.get_json(silent=True) or {}).get("text", "")
    if not text.strip():
        return jsonify({"error": "text is required"}), 400
    return jsonify(analyze_review(text))


@bp.post("/reviews/<int:review_id>")
@admin_required
def analyze_one(review_id):
    row = fetch_one("SELECT review_text FROM reviews WHERE review_id = %s",
                    (review_id,))
    if row is None:
        return jsonify({"error": "Review not found"}), 404
    result = analyze_and_store(review_id, row["review_text"])
    return jsonify({"review_id": review_id, **result})


@bp.get("/reviews/<int:review_id>")
@login_required
def get_analysis(review_id):
    analysis = fetch_one(
        "SELECT analysis_id, sentiment, sentiment_confidence, model_version, "
        "       analyzed_at FROM review_analysis WHERE review_id = %s",
        (review_id,))
    if analysis is None:
        return jsonify({"error": "No analysis for this review"}), 404
    analysis["categories"] = fetch_all(
        "SELECT category, polarity, score FROM review_analysis_categories "
        "WHERE analysis_id = %s ORDER BY score DESC",
        (analysis.pop("analysis_id"),))
    return jsonify({"review_id": review_id, **analysis})


@bp.get("/workers/<int:worker_id>")
def worker_profile(worker_id):
    """Public: aggregated strengths and weaknesses of a worker."""
    sentiment = fetch_one("SELECT * FROM v_worker_sentiment WHERE worker_id = %s",
                          (worker_id,))
    cats = fetch_all(
        "SELECT category, polarity, mentions, avg_score, pct_of_reviews "
        "FROM v_worker_category_scores WHERE worker_id = %s "
        "ORDER BY mentions DESC", (worker_id,))
    return jsonify({
        "worker_id": worker_id,
        "sentiment": sentiment or {"analyzed_reviews": 0},
        "strengths":  [c for c in cats if c["polarity"] == "positive"],
        "weaknesses": [c for c in cats if c["polarity"] == "negative"],
    })


@bp.post("/run")
@admin_required
def run_batch():
    return jsonify({"analyzed": analyze_pending()})
