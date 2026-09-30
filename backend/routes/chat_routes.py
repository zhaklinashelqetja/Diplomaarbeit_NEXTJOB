"""NextJob — KI-Chatbot (RAG me tool calling permes Groq).

Flow:  pyetja e perdoruesit -> Groq LLM me tools -> LLM kerkon te dhena ->
       ne i marrim nga MySQL -> LLM formulon pergjigjen shqip.

Endpoint:  POST /api/chat   {"message": "..."}   (login i detyrueshem)
Env:       GROQ_API_KEY, GROQ_MODEL  (/etc/nextjob/nextjob.env)
"""
import json
import os

import requests as http
from flask import Blueprint, g, jsonify, request

from auth import login_required
from db import fetch_all, fetch_one

bp = Blueprint("chat", __name__, url_prefix="/api")

GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
# Model comes from the env file, so a Groq model retirement is a config
# change, not a code change (llama-3.3-70b-versatile was shut down 2026-08-16).
GROQ_MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
MAX_TOOL_ROUNDS = 4

SYSTEM_PROMPT = """Ti je asistenti virtual i NextJob, nje platforme shqiptare \
qe lidh klientet me mjeshtra (hidraulik, elektricist, bojaxhi etj.).
Rregullat:
- Pergjigju GJITHMONE ne shqip, shkurt dhe qarte.
- Perdor tools per te marre te dhena reale nga databaza. MOS shpik te dhena.
- Kur rekomandon mjeshtra, permend piket e forta/dobëta nga analiza e \
vleresimeve (sentiment, kategori si pikepamja e cmimit, cilesia, vonesa).
- Cmimet jane ne Lek/ore nese nuk thuhet ndryshe.
- Nese pyetja s'ka lidhje me platformen, thuaj me mirësjellje qe ndihmon \
vetem per NextJob.
- Mos i trego perdoruesit emrat e tools apo detaje teknike."""

# ------------------------------------------------------------------ tools
TOOLS = [
    {"type": "function", "function": {
        "name": "search_workers",
        "description": "Kerkon mjeshtra ne platforme. Filtron sipas fjales "
                       "kyce (profesion/kategori si 'hidraulik', 'elektricist' "
                       "ose qytet). Kthen profile me cmim, vleresim mesatar etj.",
        "parameters": {"type": "object", "properties": {
            "keyword": {"type": "string",
                        "description": "profesioni, kategoria ose qyteti"},
            "sort_by": {"type": "string",
                        "enum": ["rating", "price_low", "price_high"],
                        "description": "renditja e rezultateve"}},
            "required": []}}},
    {"type": "function", "function": {
        "name": "get_worker_details",
        "description": "Profili i plote i nje mjeshtri: vleresimet e fundit "
                       "dhe analiza e sentimentit (pikat e forta/dobëta si "
                       "cmim i drejte, perpikmeri, cilesi, vonese, sjellje).",
        "parameters": {"type": "object", "properties": {
            "worker_id": {"type": "integer"}},
            "required": ["worker_id"]}}},
    {"type": "function", "function": {
        "name": "get_categories",
        "description": "Lista e te gjitha kategorive/profesioneve ne platforme.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_my_problems",
        "description": "Problemet/punet e postuara nga perdoruesi i kycur, "
                       "me statusin e tyre.",
        "parameters": {"type": "object", "properties": {}}}},
    {"type": "function", "function": {
        "name": "get_my_offers",
        "description": "Ofertat qe kane marre problemet e perdoruesit te kycur.",
        "parameters": {"type": "object", "properties": {}}}},
]


def _jsonable(rows, limit=15):
    return json.dumps(rows[:limit], default=str, ensure_ascii=False)


def run_tool(name, args, user_id):
    """Executes one tool against the database, returns a JSON string."""
    if name == "search_workers":
        rows = fetch_all("SELECT * FROM v_worker_search LIMIT 200")
        kw = (args.get("keyword") or "").strip().lower()
        if kw:
            rows = [r for r in rows if any(
                kw in str(v).lower() for v in r.values())]
        sort_by = args.get("sort_by")
        def price_key(r):
            for k in r:
                if "rate" in k or "price" in k or "cmim" in k:
                    try: return float(r[k] or 0)
                    except (TypeError, ValueError): pass
            return 0.0
        def rating_key(r):
            for k in r:
                if "rating" in k or "vler" in k:
                    try: return float(r[k] or 0)
                    except (TypeError, ValueError): pass
            return 0.0
        if sort_by == "price_low":  rows.sort(key=price_key)
        if sort_by == "price_high": rows.sort(key=price_key, reverse=True)
        if sort_by == "rating":     rows.sort(key=rating_key, reverse=True)
        return _jsonable(rows, 8) if rows else '"Nuk u gjet asnje mjeshter."'

    if name == "get_worker_details":
        wid = int(args["worker_id"])
        sentiment = fetch_one(
            "SELECT * FROM v_worker_sentiment WHERE worker_id = %s", (wid,))
        cats = fetch_all(
            """SELECT category, polarity, mentions, avg_score
               FROM v_worker_category_scores
               WHERE worker_id = %s ORDER BY mentions DESC""", (wid,))
        reviews = fetch_all(
            """SELECT r.rating, r.review_text, ra.sentiment
               FROM reviews r
               LEFT JOIN review_analysis ra ON ra.review_id = r.review_id
               WHERE r.worker_id = %s
               ORDER BY r.review_id DESC LIMIT 5""", (wid,))
        return json.dumps({
            "sentiment_permbledhje": sentiment,
            "pikat_forta": [c for c in cats if c["polarity"] == "positive"],
            "pikat_dobeta": [c for c in cats if c["polarity"] == "negative"],
            "vleresimet_e_fundit": reviews,
        }, default=str, ensure_ascii=False)

    if name == "get_categories":
        return _jsonable(fetch_all(
            "SELECT category_id, name FROM categories ORDER BY name"), 30)

    if name == "get_my_problems":
        return _jsonable(fetch_all(
            "SELECT * FROM problems WHERE customer_id = %s "
            "ORDER BY problem_id DESC LIMIT 10", (user_id,)))

    if name == "get_my_offers":
        return _jsonable(fetch_all(
            """SELECT o.* FROM offers o
               JOIN problems p ON p.problem_id = o.problem_id
               WHERE p.customer_id = %s
               ORDER BY o.offer_id DESC LIMIT 10""", (user_id,)))

    return '"Tool i panjohur."'


def call_groq(messages):
    body = {"model": GROQ_MODEL, "messages": messages,
            "tools": TOOLS, "tool_choice": "auto",
            "temperature": 0.3, "max_tokens": 1024}
    # gpt-oss models think before answering; keep that short so the
    # thinking does not eat the answer's token budget
    if GROQ_MODEL.startswith("openai/gpt-oss"):
        body["reasoning_effort"] = "low"
    resp = http.post(
        GROQ_URL,
        headers={"Authorization": f"Bearer {os.environ['GROQ_API_KEY']}",
                 "Content-Type": "application/json"},
        json=body,
        timeout=45)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]


# ------------------------------------------------------------------ route
@bp.post("/chat")
@login_required
def chat():
    d = request.get_json(silent=True) or {}
    question = (d.get("message") or "").strip()
    if not question:
        return jsonify({"error": "message is required"}), 400
    if "GROQ_API_KEY" not in os.environ:
        return jsonify({"error": "GROQ_API_KEY missing on server"}), 500

    user_id = g.user["user_id"]
    messages = [{"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question}]
    tools_used = []

    try:
        for _ in range(MAX_TOOL_ROUNDS):
            msg = call_groq(messages)
            tool_calls = msg.get("tool_calls")
            if not tool_calls:
                return jsonify({"reply": msg.get("content", ""),
                                "tools_used": tools_used})
            # send back only the standard fields (newer models add extras
            # like "reasoning" that the API does not accept as input)
            messages.append({"role": "assistant",
                             "content": msg.get("content") or "",
                             "tool_calls": tool_calls})
            for tc in tool_calls:
                fname = tc["function"]["name"]
                try:
                    fargs = json.loads(tc["function"]["arguments"] or "{}")
                except json.JSONDecodeError:
                    fargs = {}
                tools_used.append(fname)
                try:
                    result = run_tool(fname, fargs, user_id)
                except Exception as e:                     # tool failure
                    result = json.dumps({"error": str(e)})
                messages.append({"role": "tool",
                                 "tool_call_id": tc["id"],
                                 "content": result})
        return jsonify({"reply": "Me fal, s'munda ta gjej pergjigjen. "
                                 "Provo ta formulosh ndryshe.",
                        "tools_used": tools_used})
    except http.HTTPError as e:
        return jsonify({"error": f"Groq API error: "
                                 f"{e.response.status_code} "
                                 f"{e.response.text[:200]}"}), 502
    except Exception as e:
        return jsonify({"error": str(e)}), 500
