import json
import os
from getpass import getpass

import mysql.connector
from translation_service import translate_text

FIELDS = {
    "worker_profiles": ("headline", "bio"),
    "problems": ("title", "description"),
    "reviews": ("review_text",)
}

def main():
    if not os.environ.get("GROQ_API_KEY"):
        raise SystemExit("GROQ_API_KEY fehlt.")

    if os.environ.get("ENABLE_EXTERNAL_TRANSLATIONS") != "true":
        raise SystemExit("Übersetzungsdienst nicht freigegeben.")

    if input("Freigegebene Testdaten übersetzen? (JA): ") != "JA":
        return

    db = mysql.connector.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        user=os.environ.get("DB_USER", "root"),
        password=os.environ.get("DB_PASSWORD") or getpass("DB-Passwort: "),
        database=os.environ.get("DB_NAME", "nextjob")
    )

    cursor = db.cursor()
    cache = {}

    try:
        for table, fields in FIELDS.items():
            for field in fields:
                target = field + "_translations"

                cursor.execute(
                    f"SELECT DISTINCT {field} FROM {table} "
                    f"WHERE {target} IS NULL "
                    f"AND {field} IS NOT NULL "
                    f"AND {field} != ''"
                )

                rows = cursor.fetchall()

                for (original,) in rows:
                    if original not in cache:
                        result = translate_text(original)
                        if result:
                            cache[original] = result

                    result = cache.get(original)

                    if not result:
                        print(f"Übersetzung fehlgeschlagen: {table}.{field}")
                        continue

                    data = json.loads(result)

                    if not all(data.get(lang) for lang in ("de", "sq", "en")):
                        continue

                    cursor.execute(
                        f"UPDATE {table} SET {target}=%s "
                        f"WHERE BINARY {field}=BINARY %s "
                        f"AND {target} IS NULL",
                        (result, original)
                    )

                    db.commit()

                print(f"Bearbeitet: {table}.{field}")

    finally:
        cursor.close()
        db.close()

if __name__ == "__main__":
    main()
