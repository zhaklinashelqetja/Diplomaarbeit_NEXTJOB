#!/usr/bin/env bash
# ============================================================
# NextJob - rebuild the database from the SQL files in database/
#
#   sudo bash deploy/reset_db.sh           structure + test data
#   sudo bash deploy/reset_db.sh --empty   structure only
#
# File numbering in database/:
#   01-49  structure (tables, procedures, triggers, views)
#   50-99  data (seed)
#   files without a two-digit prefix are ignored
#
# The app user (nextjob_api) and its rights are NOT touched:
# MySQL keeps database grants when the database is dropped.
# ============================================================
set -euo pipefail

DB=nextjob
ADMIN_EMAIL=admin@nextjob.al

[[ $EUID -eq 0 ]] || { echo "Run with sudo."; exit 1; }

case "${1:-}" in
  "")      PATTERN='[0-9][0-9]_*.sql'; WITH_DATA=1 ;;
  --empty) PATTERN='[0-4][0-9]_*.sql'; WITH_DATA=0 ;;
  *)       echo "Usage: sudo bash $0 [--empty]"; exit 1 ;;
esac

SQL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../database" && pwd)"
shopt -s nullglob
FILES=( "$SQL_DIR"/$PATTERN )
(( ${#FILES[@]} > 0 )) || { echo "No SQL files found in $SQL_DIR"; exit 1; }

# ---- ask everything BEFORE deleting anything ----
echo "This deletes ALL data in the database '$DB' and loads:"
printf '  %s\n' "${FILES[@]##*/}"
read -rp "Type YES to continue: " answer
[[ "$answer" == "YES" ]] || { echo "Aborted, nothing changed."; exit 1; }

ADMIN_PW=""
if (( WITH_DATA )); then
  # Optional: the seed's admin password (test1234) is public in the repo.
  # Press Enter to keep it, or type a new one (min. 10 characters).
  read -rsp "New password for $ADMIN_EMAIL (Enter = keep test1234): " ADMIN_PW; echo
  if [[ -n "$ADMIN_PW" ]] && (( ${#ADMIN_PW} < 10 )); then
    echo "Too short. Aborted, nothing changed."; exit 1
  fi
fi

# ---- rebuild ----
echo "==> recreating database $DB"
mysql -e "DROP DATABASE IF EXISTS \`$DB\`;
          CREATE DATABASE \`$DB\` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

for f in "${FILES[@]}"; do
  echo "==> ${f##*/}"
  mysql --default-character-set=utf8mb4 "$DB" < "$f"
done

if [[ -n "$ADMIN_PW" ]]; then
  # same format werkzeug produces: scrypt:32768:8:1$<salt>$<hash>
  HASH="$(ADMIN_PW="$ADMIN_PW" python3 - <<'PY'
import hashlib, os, secrets, string
n, r, p = 32768, 8, 1
salt = "".join(secrets.choice(string.ascii_letters + string.digits) for _ in range(16))
h = hashlib.scrypt(os.environ["ADMIN_PW"].encode(), salt=salt.encode(),
                   n=n, r=r, p=p, maxmem=132 * n * r * p).hex()
print(f"scrypt:{n}:{r}:{p}${salt}${h}")
PY
)"
  unset ADMIN_PW
  mysql "$DB" -e "UPDATE users SET password_hash='$HASH' WHERE email='$ADMIN_EMAIL';"
  echo "==> admin password set"
fi

echo "==> done"
mysql -t "$DB" -e "
SELECT
 (SELECT COUNT(*) FROM information_schema.TABLES   WHERE TABLE_SCHEMA='$DB' AND TABLE_TYPE='BASE TABLE') AS tables_,
 (SELECT COUNT(*) FROM information_schema.VIEWS    WHERE TABLE_SCHEMA='$DB') AS views_,
 (SELECT COUNT(*) FROM information_schema.ROUTINES WHERE ROUTINE_SCHEMA='$DB') AS routines,
 (SELECT COUNT(*) FROM information_schema.TRIGGERS WHERE TRIGGER_SCHEMA='$DB') AS triggers_,
 (SELECT COUNT(*) FROM users) AS users;"
