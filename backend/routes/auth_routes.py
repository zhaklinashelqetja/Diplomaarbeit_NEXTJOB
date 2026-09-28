from flask import Blueprint, current_app, g, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from auth import (consume_link_token, create_token, issue_link_token,
                  login_required, recently_issued)
from db import execute, fetch_one
from mailer import send_password_reset, send_verification

bp = Blueprint("auth", __name__, url_prefix="/api/auth")

MIN_PASSWORD = 8


def _norm_email(value):
    return (value or "").strip().lower()


# ------------------------------------------------------ register/login

@bp.post("/register")
def register():
    d = request.get_json(silent=True) or {}
    required = ("first_name", "last_name", "email", "password")
    if not all(d.get(k) for k in required):
        return jsonify({"error": f"Required: {', '.join(required)}"}), 400
    if len(d["password"]) < MIN_PASSWORD:
        return jsonify({"error": f"Password must be at least "
                                 f"{MIN_PASSWORD} characters"}), 400

    email = _norm_email(d["email"])          # normalise ONCE, then reuse
    if fetch_one("SELECT user_id FROM users WHERE email=%s", (email,)):
        return jsonify({"error": "Email already registered"}), 409

    user_id = execute(
        "INSERT INTO users (first_name, last_name, email, password_hash, "
        "phone, location) VALUES (%s,%s,%s,%s,%s,%s)",
        (d["first_name"], d["last_name"], email,
         generate_password_hash(d["password"]),
         d.get("phone"), d.get("location")))

    token = issue_link_token(user_id, "verify_email",
                             current_app.config["VERIFY_TOKEN_HOURS"])
    send_verification(email, d["first_name"], token)

    return jsonify({"user_id": user_id,
                    "token": create_token(user_id, 0),
                    "is_verified": False}), 201


@bp.post("/login")
def login():
    d = request.get_json(silent=True) or {}
    user = fetch_one(
        "SELECT user_id, password_hash, is_active, is_verified, "
        "       token_version FROM users WHERE email=%s",
        (_norm_email(d.get("email")),))
    if user is None or not check_password_hash(user["password_hash"],
                                               d.get("password", "")):
        return jsonify({"error": "Wrong email or password"}), 401
    if not user["is_active"]:
        return jsonify({"error": "Account is deactivated"}), 403
    # Unverified users may log in - they are only blocked from posting.
    return jsonify({"user_id": user["user_id"],
                    "is_verified": bool(user["is_verified"]),
                    "token": create_token(user["user_id"],
                                          user["token_version"])})


@bp.get("/me")
@login_required
def me():
    is_worker = fetch_one(
        "SELECT user_id FROM worker_profiles WHERE user_id=%s",
        (g.user["user_id"],)) is not None
    user = {k: v for k, v in g.user.items() if k != "token_version"}
    return jsonify({**user, "is_worker": is_worker})


# ------------------------------------------------- email verification

@bp.post("/verify/request")
@login_required
def request_verification():
    """Resend the confirmation mail to the logged-in user."""
    if g.user["is_verified"]:
        return jsonify({"error": "Already verified"}), 400
    if recently_issued(g.user["user_id"], "verify_email"):
        return jsonify({"error": "A mail was just sent - please wait a "
                                 "minute before trying again"}), 429
    token = issue_link_token(g.user["user_id"], "verify_email",
                             current_app.config["VERIFY_TOKEN_HOURS"])
    send_verification(g.user["email"], g.user["first_name"], token)
    return jsonify({"sent": True})


@bp.post("/verify")
def verify_email():
    """Public: the link in the mail lands here with ?token=..."""
    token = (request.get_json(silent=True) or {}).get("token")
    user_id = consume_link_token(token, "verify_email")
    if user_id is None:
        return jsonify({"error": "Link is invalid or expired"}), 400
    execute("UPDATE users SET is_verified=TRUE WHERE user_id=%s", (user_id,))
    return jsonify({"verified": True})


# -------------------------------------------------- password reset

@bp.post("/forgot-password")
def forgot_password():
    """Always answers 200, whether or not the address exists. Anything
    else turns this endpoint into an account-enumeration oracle."""
    email = _norm_email((request.get_json(silent=True) or {}).get("email"))
    ok = {"sent": True}
    if not email:
        return jsonify(ok)

    user = fetch_one("SELECT user_id, first_name, is_active FROM users "
                     "WHERE email=%s", (email,))
    if user and user["is_active"] \
            and not recently_issued(user["user_id"], "reset_password"):
        token = issue_link_token(user["user_id"], "reset_password",
                                 current_app.config["RESET_TOKEN_HOURS"])
        send_password_reset(email, user["first_name"], token)
    return jsonify(ok)


@bp.post("/reset-password")
def reset_password():
    d = request.get_json(silent=True) or {}
    password = d.get("password") or ""
    if len(password) < MIN_PASSWORD:
        return jsonify({"error": f"Password must be at least "
                                 f"{MIN_PASSWORD} characters"}), 400

    user_id = consume_link_token(d.get("token"), "reset_password")
    if user_id is None:
        return jsonify({"error": "Link is invalid or expired"}), 400

    # token_version + 1 kills every JWT handed out before this moment
    execute("UPDATE users SET password_hash=%s, token_version=token_version+1 "
            "WHERE user_id=%s", (generate_password_hash(password), user_id))
    # any pending reset links for this account are now dead too
    execute("UPDATE auth_tokens SET used_at=UTC_TIMESTAMP() "
            "WHERE user_id=%s AND purpose='reset_password' "
            "AND used_at IS NULL", (user_id,))

    user = fetch_one("SELECT token_version FROM users WHERE user_id=%s",
                     (user_id,))
    return jsonify({"user_id": user_id,
                    "token": create_token(user_id, user["token_version"])})
