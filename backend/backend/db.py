"""Per-request MySQL connection + small query helpers.

Every route uses these helpers instead of raw connections, so
connection handling, dict rows and commits live in ONE place.
All queries use %s placeholders -> safe against SQL injection.
"""
import mysql.connector
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = mysql.connector.connect(
            host=current_app.config["DB_HOST"],
            user=current_app.config["DB_USER"],
            password=current_app.config["DB_PASSWORD"],
            database=current_app.config["DB_NAME"],
            autocommit=False,
        )
    return g.db


def close_db(_exc=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def fetch_all(sql, params=()):
    """SELECT -> list of rows, each row a dict {column: value}."""
    cur = get_db().cursor(dictionary=True)
    cur.execute(sql, params)
    rows = cur.fetchall()
    cur.close()
    return rows


def fetch_one(sql, params=()):
    """SELECT -> the first row as a dict, or None if nothing matched."""
    rows = fetch_all(sql, params)
    return rows[0] if rows else None


def execute(sql, params=()):
    """INSERT / UPDATE / DELETE. Commits and returns lastrowid."""
    db = get_db()
    cur = db.cursor()
    cur.execute(sql, params)
    db.commit()
    last_id = cur.lastrowid
    cur.close()
    return last_id


def replace_list(delete_sql, insert_sql, owner_id, ids):
    """Replace a whole M:N list in ONE transaction, e.g. a worker's trades:
    delete the old rows, insert the new ones, then commit once.
    If one id is invalid the foreign key fails and nothing is changed."""
    db = get_db()
    cur = db.cursor()
    try:
        cur.execute(delete_sql, (owner_id,))
        cur.executemany(insert_sql, [(owner_id, i) for i in ids])
        db.commit()
    except mysql.connector.Error:
        db.rollback()          # keep the old list
        raise
    finally:
        cur.close()


def call_proc(name, params=()):
    """CALL a stored procedure. SIGNAL 45000 errors bubble up
    as mysql.connector.Error and are turned into HTTP 400 by the
    global error handler in app.py."""
    db = get_db()
    cur = db.cursor()
    cur.callproc(name, params)
    db.commit()
    cur.close()
