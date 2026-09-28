"""Analyze every review that has no analysis yet - the same as
POST /api/analysis/run, but from the command line.

Uses the API's own code and settings, so it needs the same environment
variables as the API. On the server, from the backend folder:

    sudo -u nextjob bash -c 'set -a; source /etc/nextjob/nextjob.env; \
        /opt/nextjob/venv/bin/python -m ml.batch_analyze'
"""
from app import create_app
from routes.analysis_routes import analyze_pending


def main():
    with create_app().app_context():
        print(f"{analyze_pending()} reviews analyzed")


if __name__ == "__main__":
    main()
