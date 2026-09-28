"""JWT authentication + one-time links (verify email / reset password).

Flow:
  1. POST /api/auth/login -> server returns a signed token
  2. Client sends it on every request:  Authorization: Bearer <token>
  3. Decorators below decode the token and load the current user
     into flask.g.user, or reject with 401/403.

The JWT carries a `tv` (token_version) claim that is compared against
users.token_version. Bumping that column invalidates every JWT that was
already handed out - that is how a password reset logs out a thief who
already holds a valid token.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from db import execute, fetch_one


# ---------------------------------------------------------------- JWT

def create_token(user_id, token_version=0):
    payload = {
        "user_id": user_id,
        "tv": token_version,
        "exp": datetime.now(timezone.utc)
               + timedelta(hours=current_app.config["TOKEN_HOURS"]),
    }
    return jwt.encode(payload, current_app.config["SECRET_KEY"],
                      algorithm="HS256")


def _load_user_from_token():
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None, "Missing Bearer token"
    try:
        payload = jwt.decode(header[7:], current_app.config["SECRET_KEY"],
                             algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None, "Token expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"

    user = fetch_one(
        "SELECT user_id, first_name, last_name, email, phone, location, "
        "       is_admin, is_active, is_verified, token_version "
        "FROM users WHERE user_id = %s",
        (payload["user_id"],))
    if user is None or not user["is_active"]:
        return None, "User not found or deactivated"
    if payload.get("tv", 0) != user["token_version"]:
        return None, "Token no longer valid, please log in again"
    return user, None


# --------------------------------------------------------- decorators

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        # Already loaded by an outer decorator (worker_required etc.)?
        # Then skip the second decode + DB round trip.
        if getattr(g, "user", None) is None:
            user, err = _load_user_from_token()
            if err:
                return jsonify({"error": err}), 401
            g.user = user
        return f(*args, **kwargs)
    return wrapper


def optional_auth(f):
    """Sets g.user if a valid token is present, otherwise g.user = None.
    Never rejects - for public endpoints that want to log who was there."""
    @wraps(f)
    def wrapper(*args, **kwargs):
        if getattr(g, "user", None) is None:
            user, _err = _load_user_from_token()
            g.user = user
        return f(*args, **kwargs)
    return wrapper


def verified_required(f):
    """Login + confirmed email address.

    Stack it *under* login_required / worker_required, e.g.
        @worker_required
        @verified_required
        def make_offer(...)
    """
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not g.user["is_verified"]:
            return jsonify({"error": "Please confirm your email address "
                                     "first", "code": "email_unverified"}), 403
        return f(*args, **kwargs)
    return wrapper


def worker_required(f):
    """Login + must have a worker profile."""
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        wp = fetch_one("SELECT user_id FROM worker_profiles WHERE user_id=%s",
                       (g.user["user_id"],))
        if wp is None:
            return jsonify({"error": "Worker profile required"}), 403
        return f(*args, **kwargs)
    return wrapper


def admin_required(f):
    @wraps(f)
    @login_required
    def wrapper(*args, **kwargs):
        if not g.user["is_admin"]:
            return jsonify({"error": "Admin only"}), 403
        return f(*args, **kwargs)
    return wrapper


# ------------------------------------------------ one-time link tokens

def _hash(raw):
    return hashlib.sha256(raw.encode()).hexdigest()


def _utcnow():
    """Naive UTC - mysql-connector stores DATETIME without a timezone."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def issue_link_token(user_id, purpose, hours):
    """Invalidates older unused tokens of the same purpose and returns a
    fresh raw token. Only its SHA-256 hash reaches the database."""
    execute("UPDATE auth_tokens SET used_at=%s "
            "WHERE user_id=%s AND purpose=%s AND used_at IS NULL",
            (_utcnow(), user_id, purpose))
    raw = secrets.token_urlsafe(32)
    execute("INSERT INTO auth_tokens (user_id, token_hash, purpose, "
            "expires_at) VALUES (%s,%s,%s,%s)",
            (user_id, _hash(raw), purpose,
             _utcnow() + timedelta(hours=hours)))
    return raw


def consume_link_token(raw, purpose):
    """Returns user_id and burns the token, or None if it is unknown,
    already used, expired or for a different purpose."""
    if not raw:
        return None
    row = fetch_one(
        "SELECT token_id, user_id FROM auth_tokens "
        "WHERE token_hash=%s AND purpose=%s AND used_at IS NULL "
        "AND expires_at > %s",
        (_hash(raw), purpose, _utcnow()))
    if row is None:
        return None
    execute("UPDATE auth_tokens SET used_at=%s WHERE token_id=%s",
            (_utcnow(), row["token_id"]))
    return row["user_id"]


def recently_issued(user_id, purpose):
    """True if a token for this purpose was created within the cooldown -
    used to stop someone hammering 'resend mail'."""
    cutoff = _utcnow() - timedelta(
        seconds=current_app.config["RESEND_COOLDOWN_SECONDS"])
    return fetch_one(
        "SELECT token_id FROM auth_tokens "
        "WHERE user_id=%s AND purpose=%s AND created_at > %s",
        (user_id, purpose, cutoff)) is not None
