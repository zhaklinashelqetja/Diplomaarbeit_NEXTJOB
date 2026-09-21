"""NextJob REST API — Flask application factory.

Run for development:
    python app.py
Run in production (like the earlier NextJob deployment):
    gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"
"""
import os

import mysql.connector
from flask import Flask, jsonify, send_from_directory

import db
from config import Config
from routes.auth_routes import bp as auth_bp
from routes.user_routes import bp as user_bp
from routes.worker_routes import bp as worker_bp
from routes.problem_routes import bp as problem_bp
from routes.misc_routes import bp as misc_bp
from routes.analysis_routes import bp as analysis_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    for bp in (auth_bp, user_bp, worker_bp, problem_bp, misc_bp, analysis_bp):
        app.register_blueprint(bp)

    app.teardown_appcontext(db.close_db)

    # Serve uploaded images (in production nginx does this directly)
    @app.get("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # SIGNAL 45000 from stored procedures -> clean HTTP 400 JSON,
    # e.g. {"error": "Already applied"} instead of a crash
    @app.errorhandler(mysql.connector.Error)
    def handle_db_error(e):
        if getattr(e, "sqlstate", None) == "45000":
            return jsonify({"error": e.msg}), 400
        app.logger.error("DB error: %s", e)
        return jsonify({"error": "Database error"}), 500

    @app.errorhandler(404)
    def not_found(_e):
        return jsonify({"error": "Endpoint not found"}), 404

    @app.errorhandler(405)
    def wrong_method(_e):
        return jsonify({"error": "Method not allowed"}), 405

    @app.get("/api/health")
    def health():
        return jsonify({"status": "ok"})

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
