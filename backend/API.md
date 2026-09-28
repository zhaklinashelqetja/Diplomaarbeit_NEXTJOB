# NextJob REST API — Contract

Base URL: `/api` · All responses are JSON · Errors: `{"error": "..."}` with 400/401/403/404/409.

**Authentication:** after register/login the client stores the token and sends
`Authorization: Bearer <token>` on every protected request (marked 🔒 below,
👷 = requires worker profile, 🛡 = admin only).

## Auth
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| POST | `/auth/register` | first_name, last_name, email, password (min. 8), phone?, location? | 201 `{user_id, token, is_verified:false}` + sends confirmation mail |
| POST | `/auth/login` | email, password | `{user_id, token, is_verified}` |
| GET 🔒 | `/auth/me` | – | current user + `is_worker`, `is_verified` |
| POST 🔒 | `/auth/verify/request` | – | resends the confirmation mail (429 if asked again within 60 s) |
| POST | `/auth/verify` | token (from the mail link) | `{verified:true}` or 400 if invalid/expired/used |
| POST | `/auth/forgot-password` | email | always `{sent:true}` (never reveals whether the email exists) |
| POST | `/auth/reset-password` | token (from the mail link), password | new `{user_id, token}`; all older tokens stop working |

Mail links point to `FRONTEND_URL/verify-email?token=...` and
`FRONTEND_URL/reset-password?token=...`; the frontend page sends the token
to the endpoint above. Without SMTP settings the mail is written to the
server log instead of being sent.

## Users
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/users/<id>` | – | public profile |
| PUT 🔒 | `/users/me` | first_name?, last_name?, phone?, location? | updated fields |
| POST 🔒 | `/users/me/avatar` | multipart field `avatar` | `{avatar_path}` |
| GET 🔒 | `/users/me/saved-workers` | – | bookmarked workers |
| POST 🔒 | `/users/me/saved-workers/<id>` | – | 201 |
| DELETE 🔒 | `/users/me/saved-workers/<id>` | – | 200 |

## Categories
| GET | `/categories` | – | fixed trade list (Plumber, Electrician, …) |
|---|---|---|---|

## Workers
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/workers` | ?category, ?area, ?sort (avg_rating \| avg_job_price \| avg_response_hours \| completed_jobs \| years_experience), ?order, ?page, ?per_page | worker directory (v_worker_search) — the "find by price/time/quality" search |
| GET | `/workers/<id>` | – | profile + categories + latest reviews |
| POST 🔒 | `/workers/me` | headline?, bio?, years_experience?, service_area? | become a worker (201) |
| PUT 👷 | `/workers/me` | any profile field, is_available | updated fields |
| PUT 👷 | `/workers/me/categories` | `{category_ids:[...]}` | replaces trade list |
| GET 👷 | `/workers/me/feed` | – | **For You page** — refreshes + returns recommendations |
| GET 👷 | `/workers/me/offers` | – | my offers with status |
| GET 👷 | `/workers/me/jobs` | – | jobs assigned to me |
| GET 👷 | `/workers/me/saved-problems` | – | bookmarked problems |
| POST 👷 | `/workers/me/saved-problems/<id>` | – | 201 |
| DELETE 👷 | `/workers/me/saved-problems/<id>` | – | 200 |

## Problems
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET | `/problems` | ?q, ?category, ?location, ?urgency, ?status, ?page, ?per_page | list with offer_count + cover_photo (logs search) |
| GET | `/problems/<id>` | – | full detail + photos (logs view) |
| GET 🔒 | `/problems/mine` | – | my posted problems + pending offer counts |
| POST 🔒 | `/problems` | category_id, title, description, location, contact_phone, budget?, urgency?, preferred_date? | 201 `{problem_id}` |
| POST 🔒 | `/problems/<id>/photos` | multipart field `photos` (multiple) | 201 saved paths |
| PUT 🔒 | `/problems/<id>` | any field (owner, only while open) | updated fields |
| DELETE 🔒 | `/problems/<id>` | – | cancels (status change, never hard delete) |
| GET 🔒 | `/problems/<id>/offers` | – | offers incl. worker rating (owner only) |
| POST 👷 | `/problems/<id>/offers` | price, message?, initiated_by? | 201 `{offer_id}` — via `sp_make_offer` |
| PUT 🔒 | `/problems/<id>/start` | – | assigned → in_progress (customer or assigned worker) |
| PUT 🔒 | `/problems/<id>/complete` | – | → completed, via `sp_complete_problem` (owner) |
| POST 🔒 | `/problems/<id>/review` | rating 1–5, text? | 201 — via `sp_leave_review` (owner, completed only) |

## Offers
| Method | Endpoint | Returns |
|---|---|---|
| PUT 🔒 | `/offers/<id>/accept` | assigns worker + auto-rejects other offers — via `sp_accept_offer` (owner only) |
| PUT 👷 | `/offers/<id>/withdraw` | pending → withdrawn (offer owner only) |

## Messages
| Method | Endpoint | Body | Returns |
|---|---|---|---|
| GET 🔒 | `/messages/conversations` | – | chat list w/ last message + unread count |
| GET 🔒 | `/messages/<user_id>` | – | full thread (marks incoming as read) |
| POST 🔒 | `/messages/<user_id>` | content, problem_id? | 201 (also notifies receiver) |

## Notifications
| Method | Endpoint | Body / Params | Returns |
|---|---|---|---|
| GET 🔒 | `/notifications` | ?unread=1 | latest 50 |
| PUT 🔒 | `/notifications/read` | `{ids:[...]}` or empty = all | marked |

## Admin
| Method | Endpoint | Returns |
|---|---|---|
| GET 🛡 | `/admin/stats` | all statistics views in one payload (category demand, top searches, growth, top problems, top workers) |
| POST 🛡 | `/admin/reviews/detect-fakes` | runs `sp_detect_fake_reviews`, returns flagged reviews |
| PUT 🛡 | `/admin/users/<id>/deactivate` / `.../activate` | soft ban / unban |

## Review analysis (Data Science)
| Method | Endpoint | Body | Returns |
|---|---|---|---|
| POST 🔒 | `/analysis/preview` | text | sentiment + detected categories, nothing stored |
| GET 🔒 | `/analysis/reviews/<id>` | – | stored analysis of one review |
| GET | `/analysis/workers/<id>` | – | worker's sentiment + strengths / weaknesses |
| POST 🛡 | `/analysis/reviews/<id>` | – | analyze one review and store it |
| POST 🛡 | `/analysis/run` | – | analyze every review that has no analysis yet |

## Design principles
- **The API is the only door to the database.** Frontend never sees SQL or credentials.
- **Business rules live in the DB where possible** — the API calls the stored
  procedures (`sp_make_offer`, `sp_accept_offer`, `sp_complete_problem`,
  `sp_leave_review`) and translates their SIGNAL errors into clean HTTP 400 JSON.
- **Permission checks live in the API** — ownership (my problem, my offer),
  worker status, admin status; checked via decorators before any SQL runs.
- **All queries parameterized** (`%s`) → immune to SQL injection.
- **Passwords** hashed with werkzeug (never stored in plain text); auth via JWT.
- **The Python recommendation algorithm** later simply overwrites the
  `recommendations` table; `GET /workers/me/feed` needs no change.

## Running
```
pip install -r requirements.txt
export SECRET_KEY=<random> DB_USER=nextjob_api DB_PASSWORD=<password>   # see .env.example
python app.py                                          # development
gunicorn -w 4 -b 127.0.0.1:8000 "app:create_app()"     # production behind nginx
```
The app refuses to start without `SECRET_KEY`.
