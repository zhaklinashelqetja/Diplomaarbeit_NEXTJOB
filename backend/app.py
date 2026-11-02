"""NextJob REST API — Flask application factory.

Run for development:
    python app.py
Run in production (like the earlier NextJob deployment):
    gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"
"""
import os
import re

import mysql.connector
from flask import Flask, jsonify, request, send_from_directory

import db
from config import Config
from routes.auth_routes import bp as auth_bp
from routes.user_routes import bp as user_bp
from routes.worker_routes import bp as worker_bp
from routes.problem_routes import bp as problem_bp
from routes.misc_routes import bp as misc_bp
from routes.analysis_routes import bp as analysis_bp
from routes.chat_routes import bp as chat_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.json.ensure_ascii = False      # send "Shkodër", not "Shkod\u00ebr"
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(worker_bp)
    app.register_blueprint(problem_bp)
    app.register_blueprint(misc_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(chat_bp)

    app.teardown_appcontext(db.close_db)

    # The SvelteKit dev server (http://localhost:5173) runs on another
    # port, so the browser needs CORS headers to call the API. Only the
    # origins in CORS_ORIGINS are allowed. On the server, frontend and API
    # share one domain through nginx, so this is not needed there.
    @app.after_request
    def cors(resp):
        origin = request.headers.get("Origin")
        if origin and origin in app.config["CORS_ORIGINS"]:
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            resp.headers["Access-Control-Max-Age"] = "600"
        resp.vary.add("Origin")
        return resp

    # Serve uploaded images (in production nginx does this directly)
    @app.get("/uploads/<path:filename>")
    def uploads(filename):
        return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

    # Database errors -> clean JSON instead of a crash. Because the DB
    # already checks IDs, CHECKs and ENUMs, the routes don't repeat those
    # checks: a wrong neighborhood_id simply ends up here as a 400.
    @app.errorhandler(mysql.connector.Error)
    def handle_db_error(e):
        msg = e.msg or ""
        # which column was wrong? MySQL names it in the message
        found = re.search(r"(?:FOREIGN KEY \(`|column '|constraint 'chk_)(\w+)", msg, re.I)
        column = found.group(1).split("_", 1)[-1] if found and "chk_" in found.group(0) \
            else (found.group(1) if found else "value")
        column = {"exp": "years_experience"}.get(column, column)
        if getattr(e, "sqlstate", None) == "45000":   # SIGNAL from a procedure
            return jsonify({"error": msg}), 400
        if e.errno in (1216, 1452):                   # unknown foreign key id
            # the API's DB user only gets the short message (1216) without
            # the column, so then we name the usual suspects
            if column == "value":
                column = "id (check category_id / neighborhood_id)"
            return jsonify({"error": f"Unknown {column}"}), 400
        if e.errno in (1265, 1292, 1366, 3819):      # wrong ENUM/date/number/CHECK
            return jsonify({"error": f"Invalid {column}"}), 400
        if e.errno == 1048:                           # NOT NULL column missing
            return jsonify({"error": f"{column} is required"}), 400
        if e.errno == 1062:                           # UNIQUE violated
            return jsonify({"error": "Already exists"}), 409
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

    # Interactive API documentation (static/apis.html):
    # https://nextjob.htl-cloud.com/api/docs
    @app.get("/api/docs")
    def docs():
        return send_from_directory(os.path.join(app.root_path, "static"),
                                   "apis.html")

    return app


if __name__ == "__main__":
    create_app().run(debug=True, port=5000)
