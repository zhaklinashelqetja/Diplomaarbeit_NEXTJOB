"""NextJob — KI-Chatbot (RAG, pa tools).

Flow (per pyetje, pa histori bisede):
  1. Pyetja + perdoruesi i kycur (g.user) vijne ne /api/chat.
  2. EXTRACT  (Groq, thirrja 1): AI nxjerr vetem JSON me qellimin
     (intent), profesionin, lagjen, kriteret (i shpejte, i lire ...).
  3. FETCH    (Python, pa AI): sipas intent-it ekzekutohen query fikse
     dhe te sigurta ne MySQL. AI nuk prek kurre databazen.
  4. ANSWER   (Groq, thirrja 2): AI pergjigjet shqip VETEM nga te
     dhenat e marra. Nese s'ka te dhena -> e thote qarte.

  5. LOG      pyetja + pergjigjja ruhen ne ai_conversations / ai_messages.

Endpoint:  POST /api/chat   {"message": "...", "conversation_id": 7?}
           (login i detyrueshem; pa conversation_id fillon bisede e re)
Env:       GROQ_API_KEY, GROQ_MODEL  (/etc/nextjob/nextjob.env)
"""
import json
import os
import unicodedata

import requests as http
from flask import Blueprint, current_app, g, jsonify, request

from auth import login_required
from db import execute, fetch_all, fetch_one

bp = Blueprint("chat", __name__, url_prefix="/api")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
# Model comes from the env file, so a Groq model retirement is a config
# change, not a code change (llama-3.3-70b-versatile was shut down 2026-08-16).
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_QUESTION_LEN = 500
MAX_WORKERS = 5

INTENTS = {"find_workers", "worker_details", "my_problems", "my_offers",
           "my_reviews", "my_profile", "platform_stats", "off_topic"}
CRITERIA = {"fast", "cheap", "best_rated", "experienced", "available"}

OFF_TOPIC_REPLY = ("Më fal, unë ndihmoj vetëm me pyetje rreth NextJob: "
                   "gjetjen e mjeshtrave, problemet, ofertat, vlerësimet dhe "
                   "profilin tënd, si dhe statistikat e platformës.")

# review-analysis categories -> Albanian labels for the answer step
REVIEW_LABELS = {
    "price_fair": "çmim i drejtë", "punctual": "i përpiktë",
    "high_quality": "cilësi e lartë", "fast_response": "përgjigjet shpejt",
    "friendly": "i sjellshëm", "overpriced": "i shtrenjtë",
    "late": "vonohet", "poor_quality": "cilësi e dobët",
    "slow_response": "përgjigjet ngadalë", "rude": "i pasjellshëm",
}

# ------------------------------------------------------------------ prompts
EXTRACT_PROMPT = """You analyse questions sent to NextJob, an Albanian \
platform that connects customers with tradespeople. You do NOT answer the \
question. You only return one JSON object describing what the user wants.

Trade categories that exist on the platform (use the exact name or null):
{categories}

NextJob works only in Shkodër. Neighborhoods (use the exact name or null):
{neighborhoods}

Return exactly this JSON shape:
{{"intents": [], "category": null, "neighborhood": null, "criteria": [], \
"worker_name": null, "keywords": []}}

intents: 1 to 3 values, only from this list:
- "find_workers": looking for tradespeople (e.g. "hidraulik në Rus", \
"elektricist i shpejtë", "kush është bojaxhiu më i mirë")
- "worker_details": asks about one specific worker by name
- "my_problems": the user's own posted jobs/problems and their status
- "my_offers": offers on the user's problems, or offers the user sent \
as a worker
- "my_reviews": reviews the user wrote or received
- "my_profile": the user's own account or worker profile
- "platform_stats": which categories exist, demand, how many workers/jobs
- "off_topic": anything not about NextJob (weather, news, general \
knowledge, coding, other websites ...)

category: the trade asked for, mapped to one name from the list above \
(e.g. "hidraulik" -> "Plumber", "bojaxhi" -> "Painter", "elektricist" -> \
"Electrician"). null if none is asked or none fits.
neighborhood: the neighborhood from the list above if one is named \
(e.g. "te Parruca" -> "Parrucë", "në Rusi" -> "Rus"), else null. \
"Shkodër"/"Shkodra" alone is NOT a neighborhood -> null.
criteria: zero or more of
  "fast" (i shpejtë, urgjent, sa më shpejt),
  "cheap" (i lirë, çmim i ulët),
  "best_rated" (i mirë, më i miri, cilësor, i besueshëm),
  "experienced" (me përvojë),
  "available" (i disponueshëm, i lirë tani për punë).
worker_name: the worker's name if one is named, else null.
keywords: the 1-4 most important words of the question in their original \
form (e.g. ["hidraulik", "i shpejtë"])."""

ANSWER_PROMPT = """Ti je asistenti virtual i NextJob, një platformë \
shqiptare që lidh klientët me mjeshtra.
Ke marrë PYETJEN e përdoruesit dhe TË DHËNAT nga databaza e NextJob.

Rregulla të detyrueshme:
1. Përgjigju GJITHMONË në shqip, shkurt dhe qartë.
2. Përdor VETËM informacionin që ndodhet te TË DHËNAT. Mos shpik kurrë \
emra, çmime, vlerësime, qytete, data apo numra.
3. Nëse të dhënat janë bosh ose nuk e mbulojnë pyetjen, thuaje qartë, \
p.sh. "Nuk kam të dhëna për këtë në NextJob." Mos hamendëso dhe mos \
plotëso nga njohuritë e tua.
4. Nëse një pjesë e pyetjes nuk ka lidhje me NextJob, thuaj që ndihmon \
vetëm për NextJob.
5. Çmimet janë në Lek (mesatarja e ofertave të pranuara). Koha e \
përgjigjes është në orë. Vlerësimi është nga 1 deri në 5. Një vlerë null \
do të thotë që ende s'ka të dhëna; thuaje kështu, mos e quaj zero.
6. Kur rekomandon mjeshtra, shpjego pse (vlerësimi, çmimi, shpejtësia, \
pikat e forta/dobëta) sipas të dhënave.
7. Nëse te të dhënat ka "same_trade_other_areas", thuaj që në lagjen e \
kërkuar nuk punon askush, por përmend ata që punojnë në lagje të tjera.
8. Mos përmend SQL, tabela, JSON, ID apo detaje teknike.
Para se të përgjigjesh, kontrollo që çdo fakt në përgjigje ndodhet te \
TË DHËNAT."""


# ------------------------------------------------------------------ helpers
def _norm(s):
    """lowercase + strip accents, so 'Shkodër' matches 'Shkoder'."""
    s = unicodedata.normalize("NFKD", str(s or "").lower())
    return "".join(c for c in s if not unicodedata.combining(c))


def _match_neighborhood(value, neighborhoods):
    """Model answer -> exact neighborhood name, or None.
    Accepts Albanian word forms: "Rusi" -> Rus, "Parrucës" -> Parrucë
    (compares the stems without the endings -a -e -ë -i -s)."""
    if not value:
        return None
    exact = {_norm(n): n for n in neighborhoods}
    if _norm(value) in exact:
        return exact[_norm(value)]
    stem = lambda x: _norm(x).rstrip("aeis")
    hits = [n for n in neighborhoods if stem(n) == stem(value)]
    return hits[0] if len(hits) == 1 else None


def _in_clause(ids):
    return ", ".join(["%s"] * len(ids))


def call_groq(messages, *, json_mode=False, effort="low", max_tokens=800):
    body = {"model": GROQ_MODEL, "messages": messages,
            "temperature": 0.2, "max_tokens": max_tokens}
    if json_mode:
        body["response_format"] = {"type": "json_object"}
    # gpt-oss models reason before answering; the effort controls how much
    if GROQ_MODEL.startswith("openai/gpt-oss"):
        body["reasoning_effort"] = effort
    resp = http.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                 "Content-Type": "application/json"},
        json=body, timeout=45)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"].get("content") or ""


def _strengths(worker_ids):
    """Strong/weak points from the review analysis, per worker."""
    if not worker_ids:
        return {}
    rows = fetch_all(
        f"""SELECT worker_id, category, polarity, mentions
              FROM v_worker_category_scores
             WHERE worker_id IN ({_in_clause(worker_ids)})
             ORDER BY mentions DESC""", tuple(worker_ids))
    out = {wid: {"pikat_forta": [], "pikat_dobeta": []} for wid in worker_ids}
    for r in rows:
        key = "pikat_forta" if r["polarity"] == "positive" else "pikat_dobeta"
        out[r["worker_id"]][key].append(
            REVIEW_LABELS.get(r["category"], r["category"]))
    return out


# ------------------------------------------------------------------ step 2: extract
def extract(question, categories, neighborhoods):
    raw = call_groq(
        [{"role": "system",
          "content": EXTRACT_PROMPT.format(
              categories=", ".join(categories),
              neighborhoods=", ".join(neighborhoods))},
         {"role": "user", "content": question}],
        json_mode=True, effort="low", max_tokens=600)
    try:
        data = json.loads(raw.strip().strip("`").removeprefix("json"))
    except (json.JSONDecodeError, AttributeError):
        return None          # model did not return valid JSON
    if not isinstance(data, dict):
        return None

    # never trust the model's JSON blindly: keep only known values
    intents = [i for i in (data.get("intents") or []) if i in INTENTS][:3]
    cat_lookup = {c.lower(): c for c in categories}
    category = cat_lookup.get(str(data.get("category") or "").lower())
    neighborhood = _match_neighborhood(data.get("neighborhood"), neighborhoods)
    criteria = [c for c in (data.get("criteria") or []) if c in CRITERIA]
    return {
        "intents": intents or ["off_topic"],
        "category": category,
        "neighborhood": neighborhood,
        "criteria": criteria,
        "worker_name": (str(data["worker_name"]).strip() or None)
                       if data.get("worker_name") else None,
        "keywords": [str(k) for k in (data.get("keywords") or [])][:4],
    }


# ------------------------------------------------------------------ step 3: fetch
WORKER_SQL = """
SELECT ws.worker_id, ws.full_name, ws.headline, ws.neighborhood,
       ws.years_experience, ws.is_available, ws.review_count, ws.avg_rating,
       ws.completed_jobs, ws.avg_job_price, ws.avg_response_hours,
       (SELECT GROUP_CONCAT(c.name ORDER BY c.name SEPARATOR ', ')
          FROM worker_categories wc
          JOIN categories c ON c.category_id = wc.category_id
         WHERE wc.user_id = ws.worker_id)          AS categories,
       s.positive_pct
  FROM v_worker_search ws
  LEFT JOIN v_worker_sentiment s ON s.worker_id = ws.worker_id"""


def _sort_workers(rows, criteria):
    inf = float("inf")
    def num(v, missing):
        try:
            return float(v) if v is not None else missing
        except (TypeError, ValueError):
            return missing
    keys = {   # every key sorts ascending; missing values go last
        "fast":        lambda r: num(r["avg_response_hours"], inf),
        "cheap":       lambda r: num(r["avg_job_price"], inf),
        "best_rated":  lambda r: -num(r["avg_rating"], -1),
        "experienced": lambda r: -num(r["years_experience"], -1),
    }
    rows.sort(key=keys["best_rated"])            # sensible default order
    for c in reversed(criteria):                 # first criterion wins
        if c in keys:
            rows.sort(key=keys[c])
    return rows


def fetch_find_workers(ex):
    sql, params = WORKER_SQL, ()
    if ex["category"]:
        sql += """
 WHERE EXISTS (SELECT 1 FROM worker_categories wc
                 JOIN categories c ON c.category_id = wc.category_id
                WHERE wc.user_id = ws.worker_id AND c.name = %s)"""
        params = (ex["category"],)
    rows = fetch_all(sql, params)

    if "available" in ex["criteria"]:
        rows = [r for r in rows if r["is_available"]]

    other_areas = []
    if ex["neighborhood"]:      # exact match on the service areas, no text guessing
        serving = {r["user_id"] for r in fetch_all(
            """SELECT a.user_id FROM worker_service_areas a
                 JOIN neighborhoods n ON n.neighborhood_id = a.neighborhood_id
                WHERE n.name = %s""", (ex["neighborhood"],))}
        in_area = [r for r in rows if r["worker_id"] in serving]
        if not in_area and ex["category"]:
            other_areas = rows
        rows = in_area

    rows = _sort_workers(rows, ex["criteria"])[:MAX_WORKERS]
    other_areas = _sort_workers(other_areas, ex["criteria"])[:MAX_WORKERS]
    points = _strengths([r["worker_id"] for r in rows + other_areas])
    for r in rows + other_areas:
        r.update(points.get(r["worker_id"], {}))
        r.pop("worker_id", None)

    result = {"filters": {"profesioni": ex["category"],
                          "lagjja": ex["neighborhood"],
                          "kriteret": ex["criteria"]},
              "workers_found": len(rows), "workers": rows}
    if other_areas:
        result["same_trade_other_areas"] = other_areas
    return result


def fetch_worker_details(ex):
    if not ex["worker_name"]:
        return {"error": "nuk u përmend asnjë emër mjeshtri"}
    rows = fetch_all(
        WORKER_SQL + """
         WHERE ws.full_name LIKE %s
         LIMIT 3""", (f"%{ex['worker_name']}%",))
    ids = [r["worker_id"] for r in rows]
    points = _strengths(ids)
    for r in rows:
        r.update(points.get(r["worker_id"], {}))
        r["vleresimet_e_fundit"] = fetch_all(
            """SELECT r.rating, r.review_text, ra.sentiment, r.created_at
                 FROM reviews r
                 LEFT JOIN review_analysis ra ON ra.review_id = r.review_id
                WHERE r.worker_id = %s AND r.is_flagged = FALSE
                ORDER BY r.created_at DESC LIMIT 5""", (r["worker_id"],))
        r.pop("worker_id", None)
    return {"searched_name": ex["worker_name"], "workers": rows}


def fetch_my_problems(ex, user):
    return {"my_problems": fetch_all(
        """SELECT p.title, c.name AS category, n.name AS neighborhood,
                  p.budget, p.urgency, p.status, p.created_at,
                  (SELECT COUNT(*) FROM offers o
                    WHERE o.problem_id = p.problem_id) AS offers_count,
                  CONCAT(u.first_name, ' ', u.last_name) AS assigned_worker
             FROM problems p
             JOIN categories c ON c.category_id = p.category_id
             JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id
             LEFT JOIN users u ON u.user_id = p.assigned_worker_id
            WHERE p.customer_id = %s
            ORDER BY p.created_at DESC LIMIT 10""", (user["user_id"],))}


def fetch_my_offers(ex, user, is_worker):
    out = {"offers_received_on_my_problems": fetch_all(
        """SELECT p.title AS problem,
                  CONCAT(u.first_name, ' ', u.last_name) AS worker,
                  o.price, o.status, o.created_at
             FROM offers o
             JOIN problems p ON p.problem_id = o.problem_id
             JOIN users u ON u.user_id = o.worker_id
            WHERE p.customer_id = %s
            ORDER BY o.created_at DESC LIMIT 10""", (user["user_id"],))}
    if is_worker:
        out["offers_i_sent_as_worker"] = fetch_all(
            """SELECT p.title AS problem, n.name AS neighborhood, o.price,
                      o.status, o.created_at
                 FROM offers o
                 JOIN problems p ON p.problem_id = o.problem_id
                 JOIN neighborhoods n ON n.neighborhood_id = p.neighborhood_id
                WHERE o.worker_id = %s
                ORDER BY o.created_at DESC LIMIT 10""", (user["user_id"],))
    return out


def fetch_my_reviews(ex, user, is_worker):
    out = {"reviews_i_wrote": fetch_all(
        """SELECT CONCAT(u.first_name, ' ', u.last_name) AS worker,
                  p.title AS problem, r.rating, r.review_text, r.created_at
             FROM reviews r
             JOIN users u ON u.user_id = r.worker_id
             JOIN problems p ON p.problem_id = r.problem_id
            WHERE r.customer_id = %s
            ORDER BY r.created_at DESC LIMIT 10""", (user["user_id"],))}
    if is_worker:
        out["reviews_i_received"] = fetch_all(
            """SELECT p.title AS problem, r.rating, r.review_text,
                      ra.sentiment, r.created_at
                 FROM reviews r
                 JOIN problems p ON p.problem_id = r.problem_id
                 LEFT JOIN review_analysis ra ON ra.review_id = r.review_id
                WHERE r.worker_id = %s AND r.is_flagged = FALSE
                ORDER BY r.created_at DESC LIMIT 10""", (user["user_id"],))
        out.update(_strengths([user["user_id"]]).get(user["user_id"], {}))
    return out


def fetch_my_profile(ex, user, is_worker):
    out = {"account": {k: user.get(k) for k in
                       ("first_name", "last_name", "email", "phone",
                        "neighborhood", "account_type")},
           "is_worker": is_worker}
    if is_worker:
        prof = fetch_one(WORKER_SQL + " WHERE ws.worker_id = %s",
                         (user["user_id"],))
        if prof:
            prof.pop("worker_id", None)
            prof.update(_strengths([user["user_id"]]).get(user["user_id"], {}))
        succ = fetch_one(
            """SELECT total_offers, accepted_offers, acceptance_rate_pct
                 FROM v_worker_success WHERE worker_id = %s""",
            (user["user_id"],))
        out["worker_profile"] = prof
        out["offer_success"] = succ
    return out


def fetch_platform_stats(ex):
    totals = fetch_one(
        """SELECT (SELECT COUNT(*) FROM worker_profiles)          AS workers,
                  (SELECT COUNT(*) FROM worker_profiles
                    WHERE is_available = TRUE)                    AS available_workers,
                  (SELECT COUNT(*) FROM problems)                 AS problems,
                  (SELECT COUNT(*) FROM problems
                    WHERE status = 'open')                        AS open_problems""")
    return {"totals": totals,
            "categories": fetch_all(
                """SELECT name, open_problems, total_problems,
                          workers_offering
                     FROM v_category_demand""")}


def gather(ex, user):
    is_worker = user["is_worker"]
    data = {"current_user": {"first_name": user.get("first_name"),
                             "is_worker": is_worker}}
    for intent in ex["intents"]:
        if intent == "find_workers":
            data["find_workers"] = fetch_find_workers(ex)
        elif intent == "worker_details":
            data["worker_details"] = fetch_worker_details(ex)
        elif intent == "my_problems":
            data["my_problems"] = fetch_my_problems(ex, user)
        elif intent == "my_offers":
            data["my_offers"] = fetch_my_offers(ex, user, is_worker)
        elif intent == "my_reviews":
            data["my_reviews"] = fetch_my_reviews(ex, user, is_worker)
        elif intent == "my_profile":
            data["my_profile"] = fetch_my_profile(ex, user, is_worker)
        elif intent == "platform_stats":
            data["platform_stats"] = fetch_platform_stats(ex)
        elif intent == "off_topic":
            data["off_topic"] = "Kjo pjesë e pyetjes nuk ka lidhje me NextJob."
    return data


# ------------------------------------------------------------------ step 4: answer
def answer(question, data):
    payload = json.dumps(data, default=str, ensure_ascii=False)[:14000]
    return call_groq(
        [{"role": "system", "content": ANSWER_PROMPT},
         {"role": "user",
          "content": f"PYETJA:\n{question}\n\nTË DHËNAT:\n{payload}"}],
        effort="medium", max_tokens=2000)


# ------------------------------------------------------------------ step 5: log
def log_exchange(user_id, conversation_id, question, reply):
    """Saves question + answer. Without a valid conversation_id of this
    user a new conversation starts (title = start of the question).
    Returns the conversation_id so the frontend can continue it."""
    if conversation_id and not fetch_one(
            "SELECT 1 AS ok FROM ai_conversations "
            "WHERE conversation_id=%s AND user_id=%s",
            (conversation_id, user_id)):
        conversation_id = None
    if not conversation_id:
        conversation_id = execute(
            "INSERT INTO ai_conversations (user_id, title) VALUES (%s,%s)",
            (user_id, question[:150]))
    execute("INSERT INTO ai_messages (conversation_id, sender, content) "
            "VALUES (%s,'user',%s), (%s,'assistant',%s)",
            (conversation_id, question, conversation_id, reply))
    return conversation_id


# ------------------------------------------------------------------ route
@bp.post("/chat")
@login_required
def chat():
    d = request.get_json(silent=True) or {}
    question = (d.get("message") or "").strip()
    if not question:
        return jsonify({"error": "message is required"}), 400
    if len(question) > MAX_QUESTION_LEN:
        return jsonify({"error": f"Pyetja është shumë e gjatë "
                                 f"(max {MAX_QUESTION_LEN} shkronja)."}), 400
    if "GROQ_API_KEY" not in os.environ:
        return jsonify({"error": "GROQ_API_KEY missing on server"}), 500

    user = g.user
    try:
        categories = [r["name"] for r in
                      fetch_all("SELECT name FROM categories ORDER BY name")]
        neighborhoods = [r["name"] for r in
                         fetch_all("SELECT name FROM neighborhoods ORDER BY name")]
        ex = extract(question, categories, neighborhoods)
        if ex is None:
            reply = "Më fal, s'e kuptova pyetjen. Provo ta formulosh ndryshe."
        else:
            current_app.logger.warning(
                "CHAT user_id=%s intents=%s category=%s neighborhood=%s "
                "criteria=%s q=%r", user["user_id"], ex["intents"],
                ex["category"], ex["neighborhood"], ex["criteria"], question)
            if ex["intents"] == ["off_topic"]:
                reply = OFF_TOPIC_REPLY
            else:
                reply = answer(question, gather(ex, user)).strip() or \
                    "Më fal, s'munda ta formuloj përgjigjen. Provo përsëri."

        conversation_id = log_exchange(user["user_id"],
                                       d.get("conversation_id"), question, reply)
        return jsonify({"reply": reply, "extracted": ex,
                        "conversation_id": conversation_id})

    except http.HTTPError as e:
        current_app.logger.error("CHAT groq error: %s", e.response.text[:300])
        return jsonify({"error": f"Groq API error: "
                                 f"{e.response.status_code} "
                                 f"{e.response.text[:200]}"}), 502
    except Exception as e:
        current_app.logger.exception("CHAT failed")
        return jsonify({"error": str(e)}), 500
