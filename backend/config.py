import os

class Config:
    # No fallback on purpose: the repo is public, so a default key would let
    # anyone forge login tokens. The app refuses to start without it.
    SECRET_KEY     = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY is not set")
    DB_HOST        = os.environ.get("DB_HOST", "localhost")
    DB_USER        = os.environ.get("DB_USER", "root")
    DB_PASSWORD    = os.environ.get("DB_PASSWORD", "")
    DB_NAME        = os.environ.get("DB_NAME", "nextjob")
    UPLOAD_FOLDER  = os.environ.get("UPLOAD_FOLDER",
                     os.path.join(os.path.dirname(__file__), "uploads"))
    ALLOWED_IMAGES = {"png", "jpg", "jpeg", "webp"}
    MAX_CONTENT_LENGTH = 8 * 1024 * 1024   # 8 MB per request
    TOKEN_HOURS    = 24 * 7                 # JWT valid for 7 days

    # --- frontend ---------------------------------------------------
    FRONTEND_URL   = os.environ.get("FRONTEND_URL", "http://localhost:5173")

    # --- outgoing mail (Gmail: use an App Password, not the real one) -
    SMTP_HOST      = os.environ.get("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT      = int(os.environ.get("SMTP_PORT", 587))
    SMTP_USER      = os.environ.get("SMTP_USER", "")        # empty -> log only
    SMTP_PASSWORD  = os.environ.get("SMTP_PASSWORD", "")
    MAIL_FROM      = os.environ.get("MAIL_FROM",
                                    "NextJob <no-reply@nextjob.al>")

    # --- one-time link lifetimes ------------------------------------
    VERIFY_TOKEN_HOURS = 24
    RESET_TOKEN_HOURS  = 1
    RESEND_COOLDOWN_SECONDS = 60    # anti-spam for forgot-password / resend
