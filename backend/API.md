# NextJob REST API — Contract

**Try every endpoint live:** `https://nextjob.htl-cloud.com/api/docs`
(locally: `http://localhost:5000/api/docs`)

Base URL: `/api` · all responses are JSON · errors: `{"error": "..."}`

**Authentication:** register/login return a token. Send it on every protected
request as `Authorization: Bearer <token>`.
🔒 = login · 👷 = worker profile · 🛡 = admin · ✉ = email must be confirmed, otherwise 403 `{code: "email_unverified"}`

**Conventions**
- The database is English. Category names (`Plumber`, …) are translation keys;
  the frontend shows Albanian/German.
- Locations are IDs from `GET /neighborhoods` (Shkodër only), never free text.
- Prices and budgets are in Lek.
- A wrong `category_id` / `neighborhood_id`, a budget ≤ 0, an unknown
  `urgency` etc. are rejected by the database → `400 {"error": "Unknown …" / "Invalid …"}`.

## Fixed lists
| Method | Endpoint | Returns |
|---|---|---|
| GET | `/categories` | `[{category_id, name}]` |
| GET | `/neighborhoods` | `[{neighborhood_id, name, is_city_quarter, city}]` — quarters first, then the units around the city |

## Auth
| Method | Endpoint | Body | Returns |
|---|---|---|---|
| POST | `/auth/register` | first_name, last_name, email, password (min. 8), **account_type** (`jobgeber` \| `jobnehmer`), phone?, neighborhood_id? | 201 `{user_id, token, is_verified:false, account_type, is_worker}` — a jobnehmer gets an empty worker profile automatically; sends the confirmation mail |
| POST | `/auth/login` | email, password | `{user_id, token, is_verified, account_type}` |
| GET 🔒 | `/auth/me` | – | current user incl. `neighborhood_id`, `neighborhood`, `account_type`, `is_worker`, `is_verified`, `is_admin` |
| POST 🔒 | `/auth/verify/request` | – | resends the confirmation mail (429 within 60 s) |
| POST | `/auth/verify` | token | `{verified:true}` |
| POST | `/auth/forgot-password` | email | always `{sent:true}` |
| POST | `/auth/reset-password` | token, password | new `{user_id, token}`; older tokens stop working |

## Users
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/users/<id>` | – | public profile (no email/phone) |
| PUT 🔒 | `/users/me` | first_name?, last_name?, phone?, neighborhood_id? | updated fields |
| POST 🔒 | `/users/me/avatar` | multipart `avatar` | `{avatar_path}` |
| GET 🔒 | `/users/me/saved-workers` | – | bookmarked workers with rating/price/speed |
| POST / DELETE 🔒 | `/users/me/saved-workers/<id>` | – | 201 / 200 |

## Workers
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/workers` | ?category, ?neighborhood (= serves there), ?sort (avg_rating \| avg_job_price \| avg_response_hours \| completed_jobs \| years_experience), ?order, ?page, ?per_page | worker directory |
| GET | `/workers/<id>` | – | profile + categories + service_areas + last 20 reviews |
| POST 🔒 | `/workers/me` | headline?, bio?, years_experience? | become a worker (jobgeber), 409 if already one |
| PUT 👷 | `/workers/me` | headline?, bio?, years_experience?, is_available? | updated fields |
| PUT 👷 | `/workers/me/categories` | `{category_ids:[...]}` | replaces the trades (all or nothing) |
| PUT 👷 | `/workers/me/areas` | `{neighborhood_ids:[...]}` | replaces where the worker takes jobs |
| GET 👷 | `/workers/me/feed` | – | **For You**: open problem cards + `score` (trade 60 + area 30 + available 10) |
| GET 👷 | `/workers/me/offers` | – | my offers |
| GET 👷 | `/workers/me/jobs` | – | my assigned jobs incl. phone + address |
| GET 👷 | `/workers/me/saved-problems` | – | bookmarked problem cards |
| POST / DELETE 👷 | `/workers/me/saved-problems/<id>` | – | 201 / 200 |

## Problems
A **problem card** (lists, feed, saved) = `problem_id, title, budget, urgency, status, created_at, category_id, category, neighborhood_id, neighborhood, offer_count, cover_photo`.

| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/problems` | ?status (default open), ?q, ?category, ?neighborhood, ?urgency, ?page, ?per_page | problem cards (search is logged) |
| GET | `/problems/<id>` | – | full detail + photos; `contact_phone` and `address` only for the owner and the assigned worker (view is logged) |
| GET 🔒 | `/problems/mine` | – | my problem cards |
| POST 🔒✉ | `/problems` | **category_id, neighborhood_id, title, description, contact_phone**, address?, budget?, urgency?, preferred_date? | 201 `{problem_id}` |
| POST 🔒✉ | `/problems/<id>/photos` | multipart `photos` (several) | 201 saved paths |
| PUT 🔒 | `/problems/<id>` | any of the fields above (owner, only while open) | updated fields |
| DELETE 🔒 | `/problems/<id>` | – | cancels (never deletes) |
| GET 🔒 | `/problems/<id>/offers` | – | offers with worker rating, jobs, response time (owner) |
| POST 👷✉ | `/problems/<id>/offers` | price, message? | 201 `{offer_id}` — `sp_make_offer` |
| PUT 🔒 | `/problems/<id>/start` | – | assigned → in_progress |
| PUT 🔒 | `/problems/<id>/complete` | – | → completed — `sp_complete_problem` |
| POST 🔒 | `/problems/<id>/review` | rating 1–5, text? | 201 — `sp_leave_review` |

## Offers
| Method | Endpoint | Returns |
|---|---|---|
| PUT 🔒 | `/offers/<id>/accept` | assigns the worker, rejects the other offers (owner) |
| PUT 👷 | `/offers/<id>/withdraw` | pending → withdrawn (own offer) |

## Messages & notifications
| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET 🔒 | `/messages/conversations` | – | one row per partner, last message, unread |
| GET 🔒 | `/messages/<user_id>` | – | thread (marks incoming as read) |
| POST 🔒✉ | `/messages/<user_id>` | content, problem_id? | 201 `{message_id}` |
| GET 🔒 | `/notifications` | ?unread=1 | last 50 |
| PUT 🔒 | `/notifications/read` | ids? (none = all) | – |

## Chatbot
| Method | Endpoint | Body | Returns |
|---|---|---|---|
| POST 🔒 | `/chat` | message, conversation_id? | `{reply, extracted, conversation_id}` — every question + answer is saved in `ai_conversations` / `ai_messages`; send the `conversation_id` back to continue |

## Review analysis
| Method | Endpoint | Returns |
|---|---|---|
| POST 🔒 | `/analysis/preview` | analyze any `text`, nothing saved |
| GET | `/analysis/workers/<id>` | strengths / weaknesses + sentiment |
| GET 🔒 | `/analysis/reviews/<id>` | stored analysis of one review |
| POST 🛡 | `/analysis/reviews/<id>` | analyze + save one review |
| POST 🛡 | `/analysis/run` | analyze every review without a result |

## Admin
| Method | Endpoint | Returns |
|---|---|---|
| GET 🛡 | `/admin/stats` | `total_users, active_jobs, total_offers, reported_content` + category_demand, neighborhood_demand, top_searches, registration_growth, jobs_per_month, top_problems, top_workers |
| GET 🛡 | `/admin/stats/jobs-per-month` | `[{month, posted, completed, cancelled}]` |
| POST 🛡 | `/admin/reviews/detect-fakes` | runs `sp_detect_fake_reviews`, returns flagged reviews |
| PUT 🛡 | `/admin/users/<id>/deactivate` · `/activate` | – |

## System
| GET | `/health` | `{status:"ok"}` · GET `/docs` = this documentation as a clickable page |
|---|---|---|
