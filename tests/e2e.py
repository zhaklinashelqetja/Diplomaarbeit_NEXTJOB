"""End-to-end test of the NextJob API against the real seed (run against gunicorn)."""
import sys, requests
B = "http://127.0.0.1:8000"
ok = fail = 0
def check(name, cond, info=""):
    global ok, fail
    if cond: ok += 1
    else: fail += 1; print("FAIL", name, info)
def call(m, path, tok=None, **kw):
    h = {"Authorization": f"Bearer {tok}"} if tok else {}
    r = requests.request(m, B + path, headers=h, timeout=20, **kw)
    try: body = r.json()
    except Exception: body = r.text
    return r.status_code, body
def login(email, pw="test1234"):
    s, b = call("POST", "/api/auth/login", json={"email": email, "password": pw}); return b["token"]

# --- lookups / public
s, b = call("GET", "/api/health"); check("health", s == 200)
s, b = call("GET", "/api/categories"); check("categories no icon", s == 200 and len(b) == 15 and "icon" not in b[0])
s, b = call("GET", "/api/neighborhoods"); check("neighborhoods", s == 200 and len(b) == 38 and b[0]["is_city_quarter"] == 1, b[:1])
check("utf8 names", any(n["name"] == "Parrucë" for n in b))
s, b = call("GET", "/api/docs"); check("docs page", s == 200 and "<html" in b.lower() if isinstance(b, str) else False, s)

# --- auth
s, b = call("POST", "/api/auth/register", json={"first_name": "Test", "last_name": "Geber", "email": "t.geber@example.com", "password": "12345678"})
check("register needs account_type", s == 400 and "account_type" in b["error"], b)
s, b = call("POST", "/api/auth/register", json={"first_name": "Test", "last_name": "Geber", "email": "t.geber@example.com", "password": "12345678", "account_type": "admin"})
check("register bad account_type", s == 400, b)
s, b = call("POST", "/api/auth/register", json={"first_name": "Test", "last_name": "Geber", "email": "t.geber@example.com", "password": "12345678", "account_type": "jobgeber", "neighborhood_id": 999})
check("register bad neighborhood -> 400", s == 400 and "neighborhood_id" in b["error"], b)
s, b = call("POST", "/api/auth/register", json={"first_name": "Test", "last_name": "Geber", "email": "T.Geber@example.com", "password": "12345678", "account_type": "jobgeber", "neighborhood_id": 2})
check("register jobgeber", s == 201 and b["is_worker"] is False, b); tg = b["token"]
s, b = call("POST", "/api/auth/register", json={"first_name": "Test", "last_name": "Nehmer", "email": "t.nehmer@example.com", "password": "12345678", "account_type": "jobnehmer", "neighborhood_id": 3})
check("register jobnehmer -> worker", s == 201 and b["is_worker"] is True, b); tn = b["token"]
s, b = call("POST", "/api/auth/register", json={"first_name": "X", "last_name": "Y", "email": "t.geber@example.com", "password": "12345678", "account_type": "jobgeber"})
check("duplicate email 409", s == 409)
s, b = call("GET", "/api/auth/me", tg); check("me jobgeber", s == 200 and b["neighborhood"] == "Parrucë" and b["is_worker"] is False and "token_version" not in b, b)
s, b = call("GET", "/api/auth/me", tn); check("me jobnehmer", b["is_worker"] is True and b["account_type"] == "jobnehmer", b)
s, b = call("POST", "/api/auth/login", json={"email": "admin@nextjob.al", "password": "wrong"}); check("wrong pw 401", s == 401)
s, b = call("POST", "/api/auth/login", json={"email": "admin@nextjob.al", "password": "test1234"}); check("login returns account_type", s == 200 and b["account_type"] == "jobgeber", b)
admin = b["token"]
s, b = call("GET", "/api/auth/me"); check("me without token 401", s == 401)
s, b = call("POST", "/api/auth/forgot-password", json={"email": "nobody@example.com"}); check("forgot pw no oracle", s == 200 and b["sent"])
s, b = call("POST", "/api/auth/verify", json={"token": "nope"}); check("verify bad token", s == 400)
s, b = call("POST", "/api/auth/verify/request", tg); check("resend verify cooldown 429", s == 429, b)

# --- users
s, b = call("PUT", "/api/users/me", tg, json={"neighborhood_id": 5, "phone": "0691234567"}); check("update me", s == 200 and "neighborhood_id" in b["updated"], b)
s, b = call("PUT", "/api/users/me", tg, json={"neighborhood_id": 777}); check("update me bad nb", s == 400 and "neighborhood_id" in b["error"], b)
s, b = call("PUT", "/api/users/me", tg, json={"location": "Shkoder"}); check("old field ignored", s == 400)
s, b = call("GET", "/api/users/2"); check("public profile", s == 200 and b["neighborhood"] == "Perash" and "email" not in b, b)
s, b = call("POST", "/api/users/me/saved-workers/2", tg); check("save worker", s == 201)
s, b = call("GET", "/api/users/me/saved-workers", tg); check("saved workers list", s == 200 and b[0]["worker_id"] == 2 and "neighborhood" in b[0], b)
s, b = call("DELETE", "/api/users/me/saved-workers/2", tg); check("unsave worker", s == 200)

# --- workers
s, b = call("GET", "/api/workers?category=1&neighborhood=5"); check("search plumbers serving Perash", s == 200 and len(b) >= 1, b)
s, b2 = call("GET", "/api/workers?category=1"); check("neighborhood filter narrows", len(b2) >= len(b))
s, b = call("GET", "/api/workers?sort=avg_job_price&order=asc&per_page=5"); check("sort", s == 200 and len(b) == 5)
s, b = call("GET", "/api/workers/2"); check("worker profile", s == 200 and b["service_areas"] and b["categories"] and "reviews" in b, list(b)[:5])
s, b = call("GET", "/api/workers/999"); check("worker 404", s == 404)
s, b = call("PUT", "/api/workers/me/categories", tn, json={"category_ids": [1, 1, 15]}); check("set categories (dedupe)", s == 200 and b["category_ids"] == [1, 15], b)
s, b = call("PUT", "/api/workers/me/categories", tn, json={"category_ids": [1, 99]}); check("bad category -> 400, list kept", s == 400, b)
s, b = call("GET", "/api/workers/%d" % 101 if False else "/api/auth/me", tn); my_id = b["user_id"]
s, b = call("GET", f"/api/workers/{my_id}"); check("categories unchanged after failed replace", sorted(c["category_id"] for c in b["categories"]) == [1, 15], b["categories"])
s, b = call("PUT", "/api/workers/me/areas", tn, json={"neighborhood_ids": [1, 3, 5, 18]}); check("set areas", s == 200, b)
s, b = call("PUT", "/api/workers/me/areas", tn, json={"neighborhood_ids": []}); check("empty areas 400", s == 400)
s, b = call("PUT", "/api/workers/me/areas", tg, json={"neighborhood_ids": [1]}); check("areas need worker", s == 403)
s, b = call("PUT", "/api/workers/me", tn, json={"headline": "Hidraulik i ri", "years_experience": 3}); check("update worker", s == 200)
s, b = call("PUT", "/api/workers/me", tn, json={"years_experience": -2}); check("negative exp -> 400", s == 400 and "years_experience" in b["error"], b)
s, b = call("GET", "/api/workers/me/feed", tn); check("feed", s == 200 and isinstance(b, list) and (not b or ("score" in b[0] and "neighborhood" in b[0])), b[:1])
feed = b
s, b = call("POST", "/api/workers/me", tn); check("become worker twice 409", s == 409)

# --- problems (customer = tg)
# --- email verification gate (verified_required)
import re, time
s, b = call("POST", "/api/problems", tg, json={"category_id": 1, "neighborhood_id": 5, "title": "x", "description": "x", "contact_phone": "1"})
check("unverified cannot post problem", s == 403 and b.get("code") == "email_unverified", b)
s, b = call("POST", "/api/messages/2", tg, json={"content": "hi"}); check("unverified cannot message", s == 403 and b.get("code") == "email_unverified", b)
s, b = call("GET", "/api/problems?per_page=1"); pid0 = b[0]["problem_id"] if isinstance(b, list) else b["items"][0]["problem_id"]
s, b = call("POST", f"/api/problems/{pid0}/offers", tn, json={"price": 100}); check("unverified cannot offer", s == 403 and b.get("code") == "email_unverified", b)
s, b = call("GET", "/api/auth/me", tg); check("unverified can still use /me", s == 200 and b["is_verified"] is False)
def link_token(email):
    time.sleep(0.5)
    log = open("/tmp/gu.log", encoding="utf-8").read()
    i = log.rfind("mail to " + email)
    m = re.search(r"verify-email\?token=([\w\-]+)", log[i:]); return m.group(1) if m else None
for email, tok in (("t.geber@example.com", tg), ("t.nehmer@example.com", tn)):
    vt = link_token(email); check("verify link in mail " + email, vt is not None and "nextjob.htl-cloud.com/verify-email" in open("/tmp/gu.log").read())
    s, b = call("POST", "/api/auth/verify", json={"token": vt}); check("verify ok " + email, s == 200 and b["verified"], b)
    s, b = call("POST", "/api/auth/verify", json={"token": vt}); check("link single use", s == 400)
    s, b = call("GET", "/api/auth/me", tok); check("me verified " + email, b["is_verified"] is True, b)

s, b = call("POST", "/api/problems", tg, json={"category_id": 1, "title": "Test", "description": "d", "contact_phone": "069"}); check("create needs neighborhood", s == 400 and "neighborhood_id" in b["error"])
s, b = call("POST", "/api/problems", tg, json={"category_id": 1, "neighborhood_id": 5, "title": "Rrjedh rubineti", "description": "Pikon", "contact_phone": "0691234567", "budget": -5})
check("negative budget 400", s == 400 and "budget" in b["error"], b)
s, b = call("POST", "/api/problems", tg, json={"category_id": 1, "neighborhood_id": 5, "title": "Rrjedh rubineti", "description": "Pikon", "contact_phone": "0691234567", "urgency": "asap"})
check("bad urgency 400", s == 400 and "urgency" in b["error"], b)
s, b = call("POST", "/api/problems", tg, json={"category_id": 77, "neighborhood_id": 5, "title": "x", "description": "x", "contact_phone": "1"})
check("bad category 400", s == 400 and "category_id" in b["error"], b)
s, b = call("POST", "/api/problems", tg, json={"category_id": 1, "neighborhood_id": 5, "address": "Rruga Studenti 4", "title": "Rrjedh rubineti", "description": "Pikon gjithë kohën", "contact_phone": "0691234567", "budget": 2500, "urgency": "high"})
check("create problem", s == 201, b); pid = b["problem_id"]
s, b = call("GET", f"/api/problems?neighborhood=5&category=1", tg); check("list filter", s == 200 and any(p["problem_id"] == pid for p in b), b[:1])
check("card fields", {"neighborhood", "category", "offer_count", "cover_photo"} <= set(b[0]))
s, b = call("GET", f"/api/problems/{pid}"); check("detail hides phone anon", s == 200 and "contact_phone" not in b and "address" not in b and b["neighborhood"] == "Perash", list(b))
s, b = call("GET", f"/api/problems/{pid}", tg); check("detail shows phone owner", "contact_phone" in b and b["address"])
s, b = call("GET", "/api/problems/mine", tg); check("mine", s == 200 and b[0]["problem_id"] == pid)
s, b = call("PUT", f"/api/problems/{pid}", tg, json={"neighborhood_id": 3, "budget": 3000}); check("update problem", s == 200)
s, b = call("PUT", f"/api/problems/{pid}", tn, json={"budget": 1}); check("update not owner 403", s == 403)
s, b = call("GET", "/api/workers/me/feed", tn); check("new problem in new worker's feed (Rus, plumber)", any(p["problem_id"] == pid and float(p["score"]) == 100 for p in b), [(p["problem_id"], p["score"]) for p in b][:5])
# offers
s, b = call("POST", f"/api/problems/{pid}/offers", tn, json={"price": "abc"}); check("bad price 400", s == 400)
s, b = call("POST", f"/api/problems/{pid}/offers", tn, json={"price": 2800, "message": "Vij sot"}); check("make offer", s == 201, b); oid = b["offer_id"]
s, b = call("POST", f"/api/problems/{pid}/offers", tn, json={"price": 2800}); check("duplicate offer 400", s == 400 and "exists" in b["error"], b)
t2 = login("gjergj.prendi@example.com") if False else None
s, b = call("POST", f"/api/problems/{pid}/offers", tg, json={"price": 100}); check("jobgeber cannot offer 403", s == 403)
s, b = call("GET", f"/api/problems/{pid}/offers", tg); check("list offers", s == 200 and b[0]["worker"] == "Test Nehmer" and "avg_response_hours" in b[0], b)
s, b = call("GET", f"/api/problems/{pid}/offers", tn); check("offers only owner", s == 403)
s, b = call("PUT", f"/api/offers/{oid}/accept", tn); check("accept only owner", s == 403)
s, b = call("PUT", f"/api/offers/{oid}/accept", tg); check("accept", s == 200)
s, b = call("GET", f"/api/problems/{pid}", tn); check("assigned worker sees phone", "contact_phone" in b and b["status"] == "assigned")
s, b = call("GET", "/api/workers/me/jobs", tn); check("my jobs", s == 200 and b[0]["problem_id"] == pid and b[0]["address"], b[:1])
s, b = call("GET", "/api/workers/me/offers", tn); check("my offers", s == 200 and b[0]["status"] == "accepted" and b[0]["neighborhood"] == "Rus", b[:1])
s, b = call("PUT", f"/api/problems/{pid}/start", tn); check("start", s == 200)
s, b = call("POST", f"/api/problems/{pid}/review", tg, json={"rating": 5}); check("review before complete 400", s == 400)
s, b = call("PUT", f"/api/problems/{pid}/complete", tg); check("complete", s == 200)
s, b = call("POST", f"/api/problems/{pid}/review", tg, json={"rating": 9}); check("rating range", s == 400)
s, b = call("POST", f"/api/problems/{pid}/review", tg, json={"rating": 5, "text": "Erdhi shpejt, punë e pastër."}); check("review", s == 201, b)
s, b = call("POST", f"/api/problems/{pid}/review", tg, json={"rating": 5}); check("review twice 400", s == 400)
s, b = call("GET", f"/api/workers/{my_id}"); check("review on profile", b["review_count"] == 1 and float(b["avg_rating"]) == 5)
# cancel + photos
s, b = call("POST", "/api/problems", tg, json={"category_id": 2, "neighborhood_id": 1, "title": "Priza", "description": "x", "contact_phone": "1"}); p2 = b["problem_id"]
png = b"\x89PNG\r\n\x1a\n" + b"0" * 30
s, b = call("POST", f"/api/problems/{p2}/photos", tg, files=[("photos", ("a.png", png, "image/png")), ("photos", ("b.png", png, "image/png"))]); check("photos", s == 201 and len(b["photos"]) == 2, b)
s, b = call("POST", f"/api/problems/{p2}/photos", tg, files=[("photos", ("c.exe", b"x", "application/octet-stream"))]); check("photo type", s == 400)
s, b = call("DELETE", f"/api/problems/{p2}", tg); check("cancel", s == 200)
s, b = call("DELETE", f"/api/problems/{p2}", tg); check("cancel twice", s == 400)
# saved problems
s, b = call("POST", "/api/workers/me/saved-problems/140", tn); check("save problem", s == 201)
s, b = call("GET", "/api/workers/me/saved-problems", tn); check("saved problems card", s == 200 and b[0]["problem_id"] == 140 and "saved_at" in b[0] and "neighborhood" in b[0], b[:1])
s, b = call("DELETE", "/api/workers/me/saved-problems/140", tn); check("unsave problem", s == 200)
s, b = call("POST", "/api/workers/me/saved-problems/9999", tn); check("save unknown 404", s == 404)

# --- messages / notifications
s, b = call("POST", f"/api/messages/{my_id}", tg, json={"content": "Faleminderit!", "problem_id": pid}); check("send msg", s == 201)
s, b = call("GET", "/api/messages/conversations", tn); check("conversations", s == 200 and b[0]["unread"] == 1, b[:1])
s, b = call("GET", f"/api/messages/{call('GET','/api/auth/me',tg)[1]['user_id']}", tn); check("thread", s == 200 and b[-1]["content"] == "Faleminderit!")
s, b = call("GET", "/api/notifications?unread=1", tn); check("notifications", s == 200 and len(b) >= 3, len(b))
s, b = call("PUT", "/api/notifications/read", tn, json={}); check("mark read", s == 200)
s, b = call("GET", "/api/notifications?unread=1", tn); check("all read", b == [])

# --- admin
s, b = call("GET", "/api/admin/stats", tg); check("admin only", s == 403)
s, b = call("GET", "/api/admin/stats", admin); check("admin stats", s == 200 and {"total_users", "active_jobs", "total_offers", "reported_content", "jobs_per_month", "neighborhood_demand", "category_demand"} <= set(b), list(b))
s, b = call("GET", "/api/admin/stats/jobs-per-month", admin); check("jobs per month", s == 200 and len(b) >= 10 and {"month", "posted", "completed", "cancelled"} <= set(b[0]), b[:1])
s, b = call("POST", "/api/admin/reviews/detect-fakes", admin); check("detect fakes", s == 200 and any(r["customer_id"] == 99 for r in b), b[:2])
s, b = call("PUT", f"/api/admin/users/{my_id}/deactivate", admin); check("deactivate", s == 200)
s, b = call("GET", "/api/auth/me", tn); check("deactivated -> 401", s == 401)
s, b = call("PUT", f"/api/admin/users/{my_id}/activate", admin); check("activate", s == 200)

# --- analysis (model works, Albanian quality comes after retraining)
s, b = call("POST", "/api/analysis/preview", tg, json={"text": "Very fast and friendly, fair price"}); check("analysis preview", s == 200 and "sentiment" in b, b)
s, b = call("POST", "/api/analysis/run", admin); check("analysis run", s == 200 and b["analyzed"] >= 100, b)
s, b = call("GET", "/api/analysis/workers/2"); check("analysis worker", s == 200 and "strengths" in b)

# --- misc errors
s, b = call("GET", "/api/nope"); check("404 json", s == 404 and b["error"])
s, b = call("POST", "/api/categories"); check("405 json", s == 405)
print(f"\n{ok} passed, {fail} failed")
sys.exit(1 if fail else 0)
