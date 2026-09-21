"""Outgoing mail (verification + password reset).

Sending is done on a background thread so registration does not block
for the 1-3 seconds an SMTP round trip takes. If SMTP is not configured
the mail body is written to the log instead, so development works
without credentials.
"""
import smtplib
import ssl
from email.message import EmailMessage
from threading import Thread

from flask import current_app


def _send(app, to, subject, body):
    with app.app_context():
        cfg = app.config
        if not cfg.get("SMTP_USER"):
            app.logger.warning(
                "SMTP not configured - mail to %s NOT sent:\n%s", to, body)
            return
        msg = EmailMessage()
        msg["From"] = cfg["MAIL_FROM"]
        msg["To"] = to
        msg["Subject"] = subject
        msg.set_content(body)
        try:
            with smtplib.SMTP(cfg["SMTP_HOST"], cfg["SMTP_PORT"],
                              timeout=15) as s:
                s.starttls(context=ssl.create_default_context())
                s.login(cfg["SMTP_USER"], cfg["SMTP_PASSWORD"])
                s.send_message(msg)
            app.logger.info("Mail sent to %s (%s)", to, subject)
        except Exception as e:                      # never break the request
            app.logger.error("Mail to %s failed: %s", to, e)


def send_mail(to, subject, body):
    """Fire and forget. Failures are logged, never returned to the client
    (otherwise the response would leak whether an address exists)."""
    app = current_app._get_current_object()
    Thread(target=_send, args=(app, to, subject, body), daemon=True).start()


def send_verification(to, first_name, token):
    link = f"{current_app.config['FRONTEND_URL']}/verify-email?token={token}"
    send_mail(to, "Confirm your NextJob account",
              f"Hi {first_name},\n\n"
              f"Confirm your email address to start posting jobs and "
              f"making offers:\n\n{link}\n\n"
              f"The link is valid for 24 hours.\n\n"
              f"If you did not sign up for NextJob, ignore this mail.\n")


def send_password_reset(to, first_name, token):
    link = f"{current_app.config['FRONTEND_URL']}/reset-password?token={token}"
    send_mail(to, "Reset your NextJob password",
              f"Hi {first_name},\n\n"
              f"Someone asked to reset your password. Set a new one here:\n\n"
              f"{link}\n\n"
              f"The link is valid for 1 hour and can only be used once.\n\n"
              f"If this was not you, no action is needed - your current "
              f"password still works.\n")
