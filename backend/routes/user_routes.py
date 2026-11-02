import os
import uuid

from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.utils import secure_filename

from auth import login_required
from db import execute, fetch_all, fetch_one

bp = Blueprint("users", __name__, url_prefix="/api/users")


def save_image(file, subfolder):
    """Shared helper: validates + stores an uploaded image,
    returns the relative path saved in the DB."""
    ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else ""
    if ext not in current_app.config["ALLOWED_IMAGES"]:
        return None
    folder = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(folder, exist_ok=True)
    name = secure_filename(f"{uuid.uuid4().hex}.{ext}")
    file.save(os.path.join(folder, name))
    return f"/uploads/{subfolder}/{name}"


@bp.get("/<int:user_id>")
def public_profile(user_id):
    user = fetch_one(
        "SELECT u.user_id, u.first_name, u.last_name, u.account_type, "
        "       n.name AS neighborhood, u.avatar_path, u.created_at "
        "FROM users u "
        "LEFT JOIN neighborhoods n ON n.neighborhood_id = u.neighborhood_id "
        "WHERE u.user_id=%s AND u.is_active=TRUE", (user_id,))
    if user is None:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)


@bp.put("/me")
@login_required
def update_me():
    d = request.get_json(silent=True) or {}
    allowed = ("first_name", "last_name", "phone", "neighborhood_id")
    updates = {k: d[k] for k in allowed if k in d}
    if not updates:
        return jsonify({"error": "Nothing to update"}), 400
    sets = ", ".join(f"{k}=%s" for k in updates)
    execute(f"UPDATE users SET {sets} WHERE user_id=%s",
            (*updates.values(), g.user["user_id"]))
    return jsonify({"updated": list(updates)})


@bp.post("/me/avatar")
@login_required
def upload_avatar():
    file = request.files.get("avatar")
    if file is None:
        return jsonify({"error": "No file field 'avatar'"}), 400
    path = save_image(file, "avatars")
    if path is None:
        return jsonify({"error": "Only png/jpg/jpeg/webp allowed"}), 400
    execute("UPDATE users SET avatar_path=%s WHERE user_id=%s",
            (path, g.user["user_id"]))
    return jsonify({"avatar_path": path}), 201


# ---------- saved workers (customer bookmarks) ----------

@bp.get("/me/saved-workers")
@login_required
def list_saved_workers():
    # v_worker_search already has name, neighborhood, rating, price, speed
    return jsonify(fetch_all(
        "SELECT sw.saved_at, ws.* FROM saved_workers sw "
        "JOIN v_worker_search ws ON ws.worker_id = sw.worker_id "
        "WHERE sw.customer_id=%s ORDER BY sw.saved_at DESC",
        (g.user["user_id"],)))


@bp.post("/me/saved-workers/<int:worker_id>")
@login_required
def save_worker(worker_id):
    if not fetch_one("SELECT user_id FROM worker_profiles WHERE user_id=%s",
                     (worker_id,)):
        return jsonify({"error": "Worker not found"}), 404
    execute("INSERT IGNORE INTO saved_workers (customer_id, worker_id) "
            "VALUES (%s,%s)", (g.user["user_id"], worker_id))
    return jsonify({"saved": worker_id}), 201


@bp.delete("/me/saved-workers/<int:worker_id>")
@login_required
def unsave_worker(worker_id):
    execute("DELETE FROM saved_workers WHERE customer_id=%s AND worker_id=%s",
            (g.user["user_id"], worker_id))
    return jsonify({"removed": worker_id})
