# -*- coding: utf-8 -*-
"""Generate database/50_seed.sql — realistic NextJob data for Shkodër.

Run:  python3 gen_seed.py <output.sql>
Deterministic (fixed random seed), so the same file comes out every time.
"""
import random, sys, datetime as dt
from collections import defaultdict
from content import *

R = random.Random(2026)
LAUNCH = dt.datetime(2025, 11, 1, 8, 0)
NOW = dt.datetime(2026, 11, 1, 20, 0)          # data snapshot
RECENT_FROM = dt.datetime(2026, 9, 24, 7, 0)   # open/ongoing jobs start here
PW = ("scrypt:32768:8:1$Nrg69F0hLHJPAzpp$3e8583384c40aa1a1543193652734076502b69e20b"
      "59108506f233492b78e3e9ca7a99749484047c8c1d367e872436ae5951be7a5637c43a51c86fbf6b3938d5")

CITY = list(range(1, 29))          # neighborhood ids of city quarters
VELIPOJE, SHALE = 38, 36
SUMMER, WINTER = {5, 6, 7, 8, 9}, {11, 12, 1, 2, 3}

def q(v):
    if v is None: return "NULL"
    if isinstance(v, bool): return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)): return str(v)
    if isinstance(v, dt.datetime): return "'" + v.strftime("%Y-%m-%d %H:%M:%S") + "'"
    if isinstance(v, dt.date): return "'" + v.strftime("%Y-%m-%d") + "'"
    return "'" + str(v).replace("\\", "\\\\").replace("'", "''") + "'"

def rand_time(a, b):
    return a + dt.timedelta(seconds=R.randint(0, int((b - a).total_seconds())))

def day_time(d):  # realistic hour of day for a human action
    h = R.choices(range(7, 23), weights=[2, 4, 6, 7, 7, 6, 5, 5, 5, 6, 7, 7, 6, 5, 3, 2])[0]
    return d.replace(hour=h, minute=R.randint(0, 59), second=R.randint(0, 59))

def phone():
    return "06" + R.choice("789") + "".join(R.choice("0123456789") for _ in range(7))

def money(x):
    step = 500 if x >= 5000 else 100
    return float(max(step, round(x / step) * step))

# ================================================================ users
users = {}   # id -> dict
def add_user(uid, first, last, gender, acct, nb, created, admin=False, email=None):
    users[uid] = dict(user_id=uid, first=first, last=last, gender=gender, account_type=acct,
                      nb=nb, created=created, is_admin=admin, phone=phone(),
                      email=email, is_active=True)

add_user(1, "Admin", "NextJob", "m", "jobgeber", 1, dt.datetime(2025, 10, 20, 10, 0),
         admin=True, email="admin@nextjob.al")

# 30 workers: id, first, last, gender, trades, years, base nb, quality, price factor,
#             response speed (median hours), available now
W = [
    (2, "Gjergj", "Prendi", "m", [1], 22, 5, .92, 1.10, 3.0, True),
    (3, "Ilir", "Kola", "m", [1, 15], 9, 3, .85, 0.95, 2.0, True),
    (4, "Mark", "Ndoja", "m", [1], 31, 1, .90, 1.25, 9.0, True),
    (5, "Erjon", "Hysa", "m", [1, 13], 6, 7, .45, 1.05, 2.5, True),     # weak worker + fake reviews
    (6, "Sokol", "Bajraktari", "m", [15, 8, 14], 14, 32, .80, 0.85, 6.0, True),
    (7, "Dritan", "Mulaj", "m", [2], 18, 2, .90, 1.05, 4.0, True),
    (8, "Kristian", "Gjoni", "m", [2], 7, 4, .78, 0.88, 1.0, True),
    (9, "Tonin", "Pali", "m", [2, 7], 12, 6, .86, 1.00, 3.5, True),
    (10, "Fatmir", "Begolli", "m", [2], 25, 1, .93, 1.25, 14.0, True),  # great but slow
    (11, "Endrit", "Shllaku", "m", [2, 15], 4, 19, .70, 0.85, 1.5, True),
    (12, "Agron", "Daija", "m", [7], 10, 8, .88, 1.00, 3.0, True),
    (13, "Paulin", "Lazri", "m", [7, 2], 8, 3, .84, 0.95, 2.5, True),
    (14, "Xhuljan", "Toçi", "m", [7], 3, 11, .58, 0.80, 0.8, True),     # young: fast, cheap, uneven
    (15, "Pjetër", "Marku", "m", [3], 20, 9, .90, 1.10, 6.0, True),
    (16, "Bujar", "Selimi", "m", [3, 5], 15, 7, .82, 0.95, 5.0, True),
    (17, "Zef", "Pepa", "m", [3], 11, 35, .80, 0.90, 7.0, False),       # works in Montenegro since Sep
    (18, "Kolë", "Ivezaj", "m", [4], 27, 5, .91, 1.15, 10.0, True),
    (19, "Nikoll", "Frroku", "m", [4, 15, 10], 9, 16, .83, 0.95, 4.0, True),
    (20, "Rexhep", "Osmani", "m", [5], 19, 8, .85, 1.00, 8.0, True),
    (21, "Gëzim", "Kasneci", "m", [5, 11], 13, 20, .84, 1.00, 6.0, True),
    (22, "Lekë", "Dedaj", "m", [6, 5], 16, 33, .82, 1.05, 9.0, True),
    (23, "Arlind", "Spahiu", "m", [11], 8, 10, .87, 0.95, 4.0, True),
    (24, "Ndue", "Kraja", "m", [12], 21, 13, .89, 1.05, 7.0, True),
    (25, "Valon", "Mustafa", "m", [12, 15], 6, 31, .76, 0.85, 3.0, False),  # seasonal abroad
    (26, "Mimoza", "Lici", "f", [9], 10, 1, .92, 1.05, 3.0, True),
    (27, "Brikena", "Dushaj", "f", [9], 5, 38, .86, 0.90, 2.0, True),  # Velipojë rentals
    (28, "Rudina", "Kodra", "f", [9], 7, 22, .84, 0.95, 4.0, True),
    (29, "Marjan", "Kurti", "m", [13], 14, 21, .88, 1.00, 5.0, True),
    (30, "Klodian", "Jubani", "m", [14, 15], 5, 23, .80, 0.95, 3.0, True),  # jobgeber -> worker
    (31, "Viktor", "Nikolli", "m", [10, 15], 12, 24, .87, 1.00, 1.5, True), # jobgeber -> worker
]
workers = {}
for (uid, f, l, g, cats, yrs, nb, qual, pf, speed, avail) in W:
    acct = "jobgeber" if uid in (30, 31) else "jobnehmer"
    created = (rand_time(dt.datetime(2025, 11, 1, 9), dt.datetime(2025, 12, 20, 21))
               if uid not in (11, 14, 30, 31) else
               {11: dt.datetime(2026, 1, 14, 18, 2), 14: dt.datetime(2026, 2, 9, 20, 41),
                30: dt.datetime(2025, 12, 3, 19, 5), 31: dt.datetime(2025, 11, 22, 11, 30)}[uid])
    add_user(uid, f, l, g, acct, nb, created)
    prof = created + dt.timedelta(minutes=R.randint(3, 40))
    if uid == 30: prof = dt.datetime(2026, 3, 11, 17, 25)
    if uid == 31: prof = dt.datetime(2026, 4, 2, 9, 50)
    # service areas
    if nb in CITY:
        areas = {nb} | set(R.sample([n for n in CITY if n != nb], R.randint(8, 19)))
        if R.random() < .35: areas |= set(R.sample([29, 30, 31, 32, 33, 35], R.randint(1, 2)))
    elif nb == VELIPOJE:
        areas = {38, 30, 31, 29}
    else:   # villages around the city: home + neighbours + part of the city
        near = {32: [35, 33], 33: [35, 32], 35: [32, 33, 29], 31: [29, 30, 38]}[nb]
        areas = {nb, *near} | set(R.sample(CITY, R.randint(5, 12)))
    workers[uid] = dict(cats=cats, years=yrs, quality=qual, pf=pf, speed=speed, available=avail,
                        profile_created=prof, areas=sorted(areas),
                        unavailable_from=dt.datetime(2026, 9, 1) if not avail else None)

# 69 customers (ids 32-100), names unique among all users
used = {(u["first"], u["last"]) for u in users.values()}
CUST_NB_W = {1: 9, 2: 8, 3: 8, 4: 6, 5: 7, 6: 6, 7: 7, 8: 5, 9: 4, 19: 4, 20: 4, 21: 3, 22: 3,
             23: 3, 24: 3, 25: 3, 26: 2, 27: 2, 28: 2, 10: 2, 11: 2, 12: 2, 13: 2, 14: 1, 15: 1,
             16: 1, 17: 1, 18: 1, 35: 4, 32: 3, 33: 2, 30: 2, 29: 2, 31: 1, 38: 2}
for uid in range(32, 101):
    while True:
        g = R.choice("mmmff") if uid % 3 else R.choice("mf")
        f = R.choice(MALE if g == "m" else FEMALE); l = R.choice(SURNAMES)
        if (f, l) not in used: used.add((f, l)); break
    nb = R.choices(list(CUST_NB_W), weights=list(CUST_NB_W.values()))[0]
    add_user(uid, f, l, g, "jobgeber", nb, None)
# the "cousin" who writes fake reviews for worker 5
users[99].update(first="Gentian", last="Hysa", gender="m", nb=7)

# emails: reserved example.com domain, so the platform can never mail a real person
def slug(s):
    t = s.lower()
    for a, b in (("ë", "e"), ("ç", "c")): t = t.replace(a, b)
    return t
for u in users.values():
    if u["email"]: continue
    pat = R.choice(["{f}.{l}", "{f}{l}", "{f}_{l}", "{f}.{l}{n}", "{f}{n}"])
    u["email"] = pat.format(f=slug(u["first"]), l=slug(u["last"]),
                            n=R.choice([R.randint(1, 99), R.randint(1975, 2004)])) + "@example.com"
emails = set()
for u in users.values():
    while u["email"] in emails:
        u["email"] = u["email"].replace("@", str(R.randint(2, 9)) + "@")
    emails.add(u["email"])

# ================================================================ problems
GROWTH = {11: 2, 12: 3, 1: 4, 2: 5, 3: 6, 4: 7, 5: 9, 6: 12, 7: 14, 8: 15, 9: 13, 10: 0}
MONTHS = [(2025, 11), (2025, 12)] + [(2026, m) for m in range(1, 11)]

def pick_old_date(season):
    w = []
    for (y, m) in MONTHS:
        s = 1.0
        if season == "summer": s = 1.0 if m in SUMMER else .03
        if season == "winter": s = 1.0 if m in WINTER else .03
        w.append(GROWTH[m] * s)
    y, m = R.choices(MONTHS, weights=w)[0]
    start = dt.datetime(y, m, 1)
    end = (dt.datetime(y, m + 1, 1) if m < 12 else dt.datetime(y + 1, 1, 1)) - dt.timedelta(days=1)
    end = min(end, RECENT_FROM - dt.timedelta(days=3))
    return day_time(rand_time(start, end))

cat_list = [c for c, n in DEMAND.items() for _ in range(n)]
R.shuffle(cat_list)
# most AC jobs happen in summer, so keep them out of the autumn (recent) slots
cat_list.sort(key=lambda c: 1 if c == 7 and R.random() < .8 else 0)
problems = []
for i, cat in enumerate(cat_list):
    recent = i < 32
    tpls = JOBS[cat]
    if recent:
        tpls = [t for t in tpls if t[5] != "summer"] or tpls
    t = R.choice(tpls)
    if recent:
        created = day_time(rand_time(RECENT_FROM, NOW - dt.timedelta(hours=6)))
        if created > NOW - dt.timedelta(hours=2): created = NOW - dt.timedelta(hours=R.randint(3, 30))
    else:
        created = pick_old_date(t[5])
    problems.append(dict(cat=cat, tpl=t, created=created, recent=recent))

# special stories
# (a) two guesthouse jobs in Shalë (Theth) — nobody serves the mountains
for p, tpl in zip([x for x in problems if not x["recent"] and x["cat"] in (1, 2)][:2],
                  [("Bojleri i bujtinës nuk ngroh",
                    "Kemi bujtinë në Theth dhe para sezonit bojleri nuk ngroh më. Duhet dikush që vjen deri lart.",
                    3000, 6000, U_HIGH, None),
                   ("Instalim elektrik në bujtinë",
                    "Bujtinë në Theth, duhen shtuar priza dhe ndriçim në dy dhoma të reja para sezonit.",
                    15000, 30000, U_NORMAL, None)]):
    p.update(tpl=tpl, story="shale", created=day_time(rand_time(dt.datetime(2026, 4, 2), dt.datetime(2026, 5, 20))))
# (b) three small jobs of the cousin (user 99) all done by worker 5
fake = [x for x in problems if not x["recent"] and x["cat"] in (1, 13) and "story" not in x][:3]
base_day = dt.datetime(2026, 6, 8, 10, 0)
for k, p in enumerate(fake):
    p.update(story="fake", customer=99,
             tpl=[JOBS[1][1], JOBS[1][3], JOBS[13][2]][k],
             cat=[1, 1, 13][k], created=base_day + dt.timedelta(days=k * 3, hours=k))

problems.sort(key=lambda p: p["created"])
for pid, p in enumerate(problems, 1):
    p["id"] = pid

# customers: heavy users + workers who also post problems (3, 13, 20)
cust_ids = list(range(32, 101)) + [3, 13, 20, 30, 31]
cust_w = {c: 1.0 for c in cust_ids}
for c in R.sample(range(32, 99), 10): cust_w[c] = 4.0     # landlords / big families
for c in R.sample(range(32, 99), 14): cust_w[c] = 0.0     # registered, never posted
for c in (3, 13, 20): cust_w[c] = 0.4
for c in (30, 31): cust_w[c] = 0.6
cust_w[99] = 0.0
velipoje_landlords = R.sample([c for c in range(32, 99) if cust_w[c] > 0], 2)

for p in problems:
    if p.get("customer"): continue
    t = p["tpl"]
    if "Velipojë" in t[0]:
        c = R.choice(velipoje_landlords)
    elif p.get("story") == "shale":
        c = R.choice([c for c in range(32, 99) if users[c]["nb"] == SHALE] or [62])
    else:
        c = R.choices(cust_ids, weights=[cust_w[c] for c in cust_ids])[0]
    p["customer"] = c

# customer registration = before first problem
first_post = defaultdict(lambda: None)
for p in problems:
    c = p["customer"]
    if first_post[c] is None or p["created"] < first_post[c]: first_post[c] = p["created"]
for uid in range(32, 101):
    fp = first_post[uid]
    if fp:
        users[uid]["created"] = max(LAUNCH + dt.timedelta(hours=R.randint(1, 72)),
                                    fp - dt.timedelta(days=R.choice([0, 0, 0, 1, 2, 5, 9, 14]),
                                                      hours=R.randint(0, 6), minutes=R.randint(5, 59)))
    else:
        users[uid]["created"] = pick_old_date(None) if R.random() < .7 else \
            day_time(rand_time(RECENT_FROM, NOW - dt.timedelta(days=1)))
users[99]["created"] = dt.datetime(2026, 6, 7, 21, 14)
for p in problems:   # a post can never be before its author registered
    cu = users[p["customer"]]
    if p["created"] <= cu["created"]: p["created"] = cu["created"] + dt.timedelta(minutes=R.randint(10, 90))

# location, text, budget, urgency, phone
for p in problems:
    t = p["tpl"]; cu = users[p["customer"]]
    if "Velipojë" in t[0]: p["nb"] = VELIPOJE
    elif p.get("story") == "shale": p["nb"] = SHALE
    elif R.random() < .88 and cu["nb"]: p["nb"] = cu["nb"]
    else: p["nb"] = R.choice(CITY)
    p["title"] = t[0]
    extra = R.sample(EXTRAS, 2)
    p["desc"] = " ".join([t[1]] + [e.format(floor=R.choice(["dytë", "tretë", "katërt", "pestë"]))
                                    for e in extra if e]).strip()
    p["address"] = (f"{R.choice(STREETS)}, pallati {R.randint(1, 40)}" if p["nb"] in CITY and R.random() < .7
                    else None)
    p["urgency"] = R.choices(list(t[4]), weights=list(t[4].values()))[0]
    lo, hi = t[2], t[3]
    p["fair"] = R.uniform(lo, hi)                       # what the job is really worth
    p["budget"] = money(p["fair"] * R.uniform(.7, 1.05)) if R.random() < .55 else None
    p["phone"] = cu["phone"]
    p["big"] = hi >= 20000
    p["preferred"] = ((p["created"] + dt.timedelta(days=R.randint(1, 14))).date()
                      if p["urgency"] in ("low", "normal") and R.random() < .4 else None)

# ================================================================ statuses
old = [p for p in problems if not p["recent"]]
recent = [p for p in problems if p["recent"]]
for p in old: p["status"] = "completed"
cancel_pool = [p for p in old if p.get("story") is None]
for p in [x for x in old if x.get("story") == "shale"]: p["status"] = "cancelled"
for p in R.sample(cancel_pool, 11): p["status"] = "cancelled"
R.shuffle(recent)
for i, p in enumerate(sorted(recent, key=lambda x: x["created"])):
    p["status"] = "open"
by_time = sorted(recent, key=lambda x: x["created"])
for p in by_time[:12]:   # the older ones of the recent jobs are already taken
    p["status"] = "assigned"
for p in R.sample(by_time[:12], 6): p["status"] = "in_progress"

# ================================================================ offers
offers = []
def worker_ok(w, p, when):
    ww = workers[w]
    return (p["cat"] in ww["cats"] and w != p["customer"] and ww["profile_created"] < when
            and (ww["unavailable_from"] is None or when < ww["unavailable_from"]))

URG_F = {"emergency": .25, "high": .5, "normal": 1.0, "low": 1.6}
hired_before = defaultdict(set)   # customer -> workers they already hired
for p in problems:
    if p.get("story") == "shale":   # nobody came, customer gave up after ~2 weeks
        p["offers"] = []; p["updated"] = p["created"] + dt.timedelta(days=R.randint(10, 18)); continue
    pool = [w for w in workers if worker_ok(w, p, p["created"])]
    if p.get("story") == "fake":
        chosen = [5]
    else:
        if p["status"] == "cancelled":
            k = R.choice([0, 0, 1, 2])
        elif p["status"] == "open":
            k = R.choice([0, 1, 1, 2]) if p["created"] < NOW - dt.timedelta(days=2) else R.choice([0, 0, 1])
        else:
            k = R.choices([1, 2, 3], weights=[5, 4, 1])[0]
        wts = [5 if p["nb"] in workers[w]["areas"] else .6 for w in pool]
        chosen = []
        while pool and len(chosen) < k:
            w = R.choices(pool, weights=wts)[0]
            i = pool.index(w); pool.pop(i); wts.pop(i); chosen.append(w)
        if p["status"] not in ("open", "cancelled") and not chosen:
            alt = [w for w in workers if p["cat"] in workers[w]["cats"] and w != p["customer"]
                   and workers[w]["profile_created"] < p["created"]
                   and (workers[w]["unavailable_from"] is None or p["created"] < workers[w]["unavailable_from"])]
            if alt:
                chosen = [R.choice(alt)]
            else:   # nobody on the platform could do this job yet
                p["status"] = "open" if p["recent"] else "cancelled"
    plist = []
    for w in chosen:
        ww = workers[w]
        direct = (w in hired_before[p["customer"]] and R.random() < .6) or R.random() < .08
        delay_h = ww["speed"] * URG_F[p["urgency"]] * R.lognormvariate(0, .55)
        if direct: delay_h = R.uniform(.3, 6)   # customer wrote first, worker answered
        made = p["created"] + dt.timedelta(minutes=max(8, int(delay_h * 60)))
        if made > NOW - dt.timedelta(minutes=30): made = NOW - dt.timedelta(minutes=R.randint(30, 300))
        price = money(p["fair"] * ww["pf"] * R.uniform(.88, 1.12))
        plist.append(dict(problem=p["id"], worker=w, price=price, created=made,
                          initiated_by="customer" if direct else "worker",
                          message=R.choice(OFFER_MSGS), status="pending"))
    p["offers"] = plist
    # choose the accepted one: quality and price both matter
    if p["status"] in ("completed", "assigned", "in_progress"):
        if p.get("story") == "fake":
            best = plist[0]
        else:
            def score(o):
                ww = workers[o["worker"]]
                return ww["quality"] * 2.2 - o["price"] / p["fair"] + R.uniform(-.4, .4) + \
                       (.8 if o["worker"] in hired_before[p["customer"]] else 0)
            best = max(plist, key=score)
        last_offer = max(o["created"] for o in plist)
        p["accepted_at"] = last_offer + dt.timedelta(minutes=R.randint(20, 18 * 60))
        if p["accepted_at"] > NOW: p["accepted_at"] = NOW - dt.timedelta(minutes=20)
        best["status"] = "accepted"; best["changed"] = p["accepted_at"]
        for o in plist:
            if o is not best:
                o["status"] = "rejected"; o["changed"] = p["accepted_at"]
        p["worker"] = best["worker"]; p["price"] = best["price"]
        hired_before[p["customer"]].add(best["worker"])
        dur = dt.timedelta(days=R.randint(4, 18)) if p["big"] else dt.timedelta(hours=R.randint(3, 70))
        if p["preferred"]:
            dur = max(dur, dt.datetime.combine(p["preferred"], dt.time(9)) - p["accepted_at"])
        if p["status"] == "completed":
            p["completed_at"] = day_time(p["accepted_at"] + dur)
            if p["completed_at"] >= RECENT_FROM: p["completed_at"] = RECENT_FROM - dt.timedelta(hours=R.randint(5, 60))
            if p["completed_at"] <= p["accepted_at"]: p["completed_at"] = p["accepted_at"] + dt.timedelta(hours=R.randint(2, 8))
            p["updated"] = p["completed_at"]
        elif p["status"] == "in_progress":
            p["started_at"] = min(NOW - dt.timedelta(hours=1), p["accepted_at"] + dt.timedelta(hours=R.randint(4, 40)))
            p["updated"] = p["started_at"]
        else:
            p["updated"] = p["accepted_at"]
    elif p["status"] == "cancelled":
        last = max([o["created"] for o in plist], default=p["created"])
        p["updated"] = last + dt.timedelta(days=R.randint(1, 9))
        for o in plist:
            if R.random() < .3: o["status"] = "withdrawn"; o["changed"] = o["created"] + dt.timedelta(hours=R.randint(5, 60))
            else: o["status"] = "rejected"; o["changed"] = p["updated"]
    else:
        p["updated"] = max([o["created"] for o in plist], default=p["created"])
    offers.extend(plist)
offers.sort(key=lambda o: o["created"])
for oid, o in enumerate(offers, 1): o["id"] = oid

# ================================================================ reviews
def phrase(s, g):
    return (s.replace("{A}", "I" if g == "m" else "E").replace("{a}", "i" if g == "m" else "e")
             .replace("{nice}", "sjellshëm" if g == "m" else "sjellshme")
             .replace("{kenaq}", "i kënaqur" if g == "m" else "e kënaqur"))

def rating_for(w):
    ql = workers[w]["quality"]
    probs = [max(.01, x) for x in (
        .02 + (1 - ql) * .25, .02 + (1 - ql) * .22, .05 + (1 - ql) * .25, .15 + (1 - ql) * .1, ql * .8)]
    return R.choices([1, 2, 3, 4, 5], weights=probs)[0]

def review_text(rating, w, cust):
    wg, cg = users[w]["gender"], users[cust]["gender"]
    aspects = R.sample(list(ASPECTS), R.choice([1, 2, 2, 3]))
    parts, labels = [], []
    for a in aspects:
        pos = (rating >= 4) or (rating == 3 and R.random() < .5)
        if rating <= 2: pos = R.random() < .15
        txt = R.choice(ASPECTS[a][0 if pos else 1])
        parts.append(phrase(txt, wg)); labels.append(ASPECT_LABELS[a][0 if pos else 1])
    if rating >= 4: o, c = R.choice(OPEN_POS), R.choice(CLOSE_POS)
    elif rating == 3: o, c = R.choice(OPEN_MID), R.choice(CLOSE_MID)
    else: o, c = R.choice(OPEN_NEG), R.choice(CLOSE_NEG)
    text = " ".join(x for x in [phrase(o, cg)] + parts + [c] if x)
    return text, labels

reviews, seen = [], set()
done = [p for p in problems if p["status"] == "completed"]
skip = set(R.sample([p["id"] for p in done if p.get("story") != "fake"], max(0, len(done) - 100)))
for p in done:
    if p["id"] in skip: continue
    w, c = p["worker"], p["customer"]
    if p.get("story") == "fake":
        rating = 5
        text = R.choice(["Mjeshtër shumë i mirë, punë e shkëlqyer!", "Më i miri në Shkodër!!!",
                         "Punë perfekte, shumë i shpejtë dhe i lirë, e rekomandoj 100%!"])
        while text in seen: text += "!"
        last_done = max(x["completed_at"] for x in problems if x.get("story") == "fake")
        created = (last_done + dt.timedelta(days=1)).replace(hour=22, minute=5, second=12) + \
                  dt.timedelta(minutes=17 * len([r for r in reviews if r["customer"] == 99]))
        labels = ["high_quality", "fast_response", "price_fair"]
    else:
        rating = rating_for(w)
        for _ in range(50):
            text, labels = review_text(rating, w, c)
            if text not in seen: break
        if R.random() < .05: text, labels = None, []          # stars only
        created = p["completed_at"] + dt.timedelta(minutes=R.randint(40, 60 * 24 * 4))
        if created >= NOW: created = NOW - dt.timedelta(hours=2)
    if text: seen.add(text)
    reviews.append(dict(problem=p["id"], worker=w, customer=c, rating=rating, text=text,
                        created=created, labels=labels))
# copy-paste review: same text from two different customers (trigger flags the 2nd)
cands = [r for r in reviews if r["customer"] != 99 and r["rating"] == 5 and r["text"]]
cands.sort(key=lambda r: r["created"])
dup_text = "Punë shumë e mirë, e rekomandoj!"
cands[10]["text"] = dup_text; cands[-6]["text"] = dup_text
reviews.sort(key=lambda r: r["created"])
for rid, r in enumerate(reviews, 1): r["id"] = rid
assert len(reviews) == 100, len(reviews)

# ================================================================ photos (100)
photos = []
with_photo = [p for p in problems if R.random() < .55]
for p in with_photo:
    n = R.choices([1, 2, 3], weights=[6, 3, 1])[0]
    for k in range(n):
        photos.append(dict(problem=p["id"], k=k, uploaded=p["created"] + dt.timedelta(seconds=20 + 8 * k)))
photos = photos[:100]
while len(photos) < 100:
    p = R.choice(problems)
    k = len([x for x in photos if x["problem"] == p["id"]])
    photos.append(dict(problem=p["id"], k=k, uploaded=p["created"] + dt.timedelta(seconds=20 + 8 * k)))
photos.sort(key=lambda x: (x["problem"], x["k"]))
for i, ph in enumerate(photos, 1):
    ph["id"] = i
    ph["path"] = f"/uploads/problems/seed_p{ph['problem']}_{ph['k'] + 1}.jpg"

# ================================================================ messages (100)
messages = []
jobs = [p for p in problems if p["status"] in ("completed", "assigned", "in_progress")]
for p in R.sample(jobs, 25):
    w, c = p["worker"], p["customer"]
    a, b = R.sample(CHAT, 2)
    t = p["accepted_at"] + dt.timedelta(minutes=R.randint(10, 120))
    end = p.get("completed_at") or NOW
    for (q_, a_) in (a, b):
        for (s, rcv, txt) in ((c, w, q_), (w, c, a_)):
            txt = txt.format(street=p["address"] or R.choice(STREETS), floor=R.choice(["dytë", "tretë", "katërt"]))
            messages.append(dict(sender=s, receiver=rcv, problem=p["id"], content=txt,
                                 sent=min(t, NOW - dt.timedelta(minutes=5))))
            t += dt.timedelta(minutes=R.randint(2, 180))
messages.sort(key=lambda m: m["sent"])
for i, m in enumerate(messages, 1):
    m["id"] = i; m["read"] = m["sent"] < NOW - dt.timedelta(days=2) or R.random() < .5

# ================================================================ views, saves, searches
views = []
for p in problems:
    who = [o["worker"] for o in p["offers"]]
    for o in p["offers"]:
        views.append((p["id"], o["worker"], o["created"] - dt.timedelta(minutes=R.randint(2, 50))))
    others = [w for w in workers if p["cat"] in workers[w]["cats"] and w not in who and w != p["customer"]]
    for _ in range(R.randint(1, 5)):
        if others and R.random() < .7:
            w = R.choice(others)
        else:
            w = None   # visitor without login
        tv = p["created"] + dt.timedelta(minutes=R.randint(5, 60 * 72))
        if tv < NOW: views.append((p["id"], w, tv))
views.sort(key=lambda v: v[2])

saved_w = set(); saved_w_rows = []
custs = [p["customer"] for p in problems]
while len(saved_w_rows) < 100:
    c = R.choice(range(32, 101)); w = R.choice(list(workers))
    hired = [p for p in problems if p["customer"] == c and p.get("worker")]
    if hired and R.random() < .6: w = R.choice(hired)["worker"]; when = hired[0]["accepted_at"] + dt.timedelta(hours=R.randint(1, 200))
    else: when = rand_time(max(users[c]["created"], workers[w]["profile_created"]), NOW)
    if (c, w) in saved_w or c == w or when > NOW: continue
    saved_w.add((c, w)); saved_w_rows.append((c, w, when))

saved_p = set(); saved_p_rows = []
while len(saved_p_rows) < 100:
    p = R.choice(problems)
    pool = [w for w in workers if p["cat"] in workers[w]["cats"] and w != p["customer"]
            and workers[w]["profile_created"] < p["created"]]
    if not pool: continue
    w = R.choice(pool); when = p["created"] + dt.timedelta(minutes=R.randint(10, 3000))
    if (w, p["id"]) in saved_p or when > NOW: continue
    saved_p.add((w, p["id"])); saved_p_rows.append((w, p["id"], when))

KEYWORDS = {1: ["hidraulik", "bojler", "rubinet", "hidraulk", "rrjedh uji"], 2: ["elektricist", "rrymë", "siguresa", "elektrik"],
            3: ["bojaxhi", "lyerje", "myk"], 4: ["marangoz", "parket"], 5: ["murator", "lagështi"], 6: ["çati", "ulluqe"],
            7: ["kondicioner", "kondicjoner", "klima", "gaz kondicioneri"], 8: ["kopshtar"], 9: ["pastrim", "pastruese"],
            10: ["çelësbërës", "bravë"], 11: ["pllaka", "pllakashtrues"], 12: ["saldator", "kangjella"],
            13: ["lavatriçe", "frigorifer"], 14: ["transport", "trasport mobilie"], 15: ["montim", "mjeshtër"]}
searches = []
for _ in range(100):
    cat = R.choices(list(DEMAND), weights=list(DEMAND.values()))[0]
    when = pick_old_date(None) if R.random() < .8 else rand_time(RECENT_FROM, NOW)
    u = R.choice([None, None] + [x for x in range(32, 101) if users[x]["created"] < when])
    mode = R.random()
    kw = R.choice(KEYWORDS[cat]) if mode < .7 else None
    cf = cat if mode >= .5 else None
    nf = (users[u]["nb"] if u and R.random() < .5 else R.choice(CITY)) if R.random() < .4 else None
    if kw is None and cf is None: cf = cat
    searches.append((u, kw, cf, nf, when))
searches.sort(key=lambda s: s[4])

# ================================================================ AI chatbot log (50 / 100)
CAT_SQ = {1: "hidraulik", 2: "elektricist", 3: "bojaxhi", 4: "marangoz", 5: "murator", 6: "mjeshtër çatie",
          7: "teknik kondicioneri", 8: "kopshtar", 9: "pastruese", 10: "çelësbërës", 11: "pllakashtrues",
          12: "saldator", 13: "riparues elektroshtëpiakesh", 14: "transportues", 15: "mjeshtër"}
NB = {}
def stats_for(w, until):
    rs = [r["rating"] for r in reviews if r["worker"] == w and r["created"] < until and r["customer"] != 99]
    return (round(sum(rs) / len(rs), 1), len(rs)) if rs else (None, 0)
convs, ai_msgs = [], []
asked = R.sample([u for u in range(32, 101) if users[u]["created"] < NOW - dt.timedelta(days=5)], 50)
for uid in asked:
    start = rand_time(max(users[uid]["created"], dt.datetime(2026, 2, 1)), NOW - dt.timedelta(hours=3))
    cat = R.choices(list(DEMAND), weights=list(DEMAND.values()))[0]
    nbn = users[uid]["nb"]
    kind = R.choice(["find", "find", "find", "price", "how"])
    if kind == "find":
        title = f"Kërkoj {CAT_SQ[cat]}"
        qtxt = f"Kam nevojë për një {CAT_SQ[cat]} afër meje. Kush është më i miri?"
        cand = [w for w in workers if cat in workers[w]["cats"] and workers[w]["profile_created"] < start
                and (workers[w]["unavailable_from"] is None or start < workers[w]["unavailable_from"])]
        ranked = sorted(cand, key=lambda w: -(stats_for(w, start)[0] or 0))[:2]
        if ranked:
            lines = []
            for w in ranked:
                avg, n = stats_for(w, start)
                s = f"{users[w]['first']} {users[w]['last']}"
                lines.append(f"{s} ({avg} yje nga {n} {'vlerësim' if n == 1 else 'vlerësime'})" if n else f"{s} (ende pa vlerësime)")
            atxt = "Në platformë gjeta: " + " dhe ".join(lines) + ". Mund t'u shkruani direkt nga profili i tyre."
        else:
            atxt = f"Për momentin nuk ka asnjë {CAT_SQ[cat]} të lirë në platformë. Provoni të postoni problemin, punëtorët njoftohen automatikisht."
    elif kind == "price":
        t = R.choice(JOBS[cat]); title = "Sa kushton?"
        ps = [o["price"] for o in offers if problems[o["problem"] - 1]["cat"] == cat
              and o["status"] == "accepted" and o["created"] < start]
        qtxt = f"Sa kushton afërsisht: {t[0].lower()}?"
        avg_txt = f"{int(round(sum(ps) / len(ps), -2)):,}".replace(",", ".") if ps else ""
        atxt = (f"Për punë të këtij lloji ofertat e pranuara në platformë kanë qenë mesatarisht rreth {avg_txt} lekë. Çmimi i saktë varet nga puna, ndaj postoni problemin për oferta."
                if len(ps) >= 3 else "Nuk kam ende mjaftueshëm të dhëna për këtë lloj pune. Postoni problemin dhe do merrni oferta me çmim.")
    else:
        title = "Si funksionon?"
        qtxt = R.choice(["Si mund të postoj një problem?", "A paguaj diçka për të postuar?", "Si e zgjedh punëtorin?"])
        atxt = R.choice(["Shtypni 'Posto problem', zgjidhni kategorinë dhe lagjen, shtoni foto dhe përshkrim. Punëtorët që punojnë në atë zonë ju dërgojnë oferta.",
                         "Postimi i problemit është falas. Paguani vetëm punëtorin që zgjidhni, sipas ofertës.",
                         "Krahasoni ofertat: çmimin, vlerësimet me yje dhe sa shpejt përgjigjet punëtori. Pastaj pranoni ofertën që ju përshtatet."])
    convs.append(dict(user=uid, title=title, started=start))
    ai_msgs.append(dict(conv=len(convs), sender="user", content=qtxt, sent=start))
    ai_msgs.append(dict(conv=len(convs), sender="assistant", content=atxt, sent=start + dt.timedelta(seconds=R.randint(2, 6))))
order = sorted(range(len(convs)), key=lambda i: convs[i]["started"])
remap = {old + 1: new + 1 for new, old in enumerate(order)}
convs = [convs[i] for i in order]
for m in ai_msgs: m["conv"] = remap[m["conv"]]
ai_msgs.sort(key=lambda m: (m["conv"], m["sent"]))

# ================================================================ notifications (mirror the triggers)
notifs = []
def notify(u, typ, msg, when):
    notifs.append(dict(user=u, type=typ, msg=msg, when=when))
pmap = {p["id"]: p for p in problems}
for o in offers:
    p = pmap[o["problem"]]
    notify(p["customer"], "offer", f"New offer ({o['price']:.2f} ALL) on your problem #{p['id']}", o["created"])
    if o["status"] != "pending":
        notify(o["worker"], "offer", f"Your offer on problem #{p['id']} is now: {o['status']}", o["changed"])
for p in problems:
    if p.get("worker"):
        notify(p["worker"], "job", f"Job #{p['id']} is now: assigned", p["accepted_at"])
        if p["status"] == "in_progress":
            notify(p["worker"], "job", f"Job #{p['id']} is now: in_progress", p["started_at"])
        if p["status"] == "completed":
            notify(p["worker"], "job", f"Job #{p['id']} is now: completed", p["completed_at"])
            notify(p["customer"], "review", f"Job #{p['id']} completed — leave a review for the worker!", p["completed_at"])
for r in reviews:
    notify(r["worker"], "review", f"You received a {r['rating']}-star review", r["created"])
notifs.sort(key=lambda n: n["when"])
for n in notifs: n["read"] = n["when"] < NOW - dt.timedelta(days=4) or R.random() < .3

# ================================================================ write SQL
out = []
w = out.append
w("""-- ============================================================
-- NextJob — realistic seed data for Shkodër (generated by gen_seed.py)
-- Loaded by deploy/reset_db.sh after 01-03 on a FRESH database.
--
-- * Every account's password is:  test1234   (admin: set a new one in reset_db.sh)
-- * Emails use example.com on purpose: the platform can never mail a real person.
-- * Phone numbers have the real Albanian format but are random: do not call them.
-- * Prices are in Lek (2026 level). Texts are in Albanian, like real users write.
-- * Story lines inside the data (for the thesis / demos):
--     - worker 5 gets three 5-star reviews from his cousin (user 99) within
--       one hour -> run CALL sp_detect_fake_reviews() to catch them
--     - two customers posted the same copy-paste review -> flagged by trigger
--     - two guesthouse jobs in Shalë (Theth) got no offer: nobody serves the mountains
--     - workers 17 and 25 work seasonally in Montenegro since September (unavailable)
-- ============================================================
USE nextjob;
SET @pw = '""" + PW + "';\n")

def insert(table, cols, rows, chunk=50):
    for i in range(0, len(rows), chunk):
        w(f"INSERT INTO {table} ({', '.join(cols)}) VALUES")
        w(",\n".join("(" + ", ".join(r) + ")" for r in rows[i:i + chunk]) + ";")
    w("")

w("-- ---------- users (1 admin, 30 workers, 69 customers) ----------")
rows = []
for uid in sorted(users):
    u = users[uid]
    rows.append([q(uid), q(u["is_admin"]), q(u["account_type"]), q(u["first"]), q(u["last"]), q(u["email"]),
                 "@pw", q(u["phone"]), q(u["nb"]), "NULL", q(u["is_active"]), "TRUE", "0",
                 q(u["created"]), q(u["created"])])
insert("users", ["user_id", "is_admin", "account_type", "first_name", "last_name", "email", "password_hash",
                 "phone", "neighborhood_id", "avatar_path", "is_active", "is_verified", "token_version",
                 "created_at", "updated_at"], rows)

w("-- ---------- worker profiles ----------")
rows = []
for uid in sorted(workers):
    ww = workers[uid]
    head = R.choice(HEADLINES[ww["cats"][0]])
    bio = R.choice(BIOS).format(y=ww["years"])
    if not ww["available"]: bio += " Nga shtatori punoj sezonalisht në Mal të Zi, kthehem në pranverë."
    rows.append([q(uid), q(head), q(bio), q(ww["years"]), q(ww["available"]), q(ww["profile_created"])])
insert("worker_profiles", ["user_id", "headline", "bio", "years_experience", "is_available", "created_at"], rows)

w("-- ---------- worker trades ----------")
insert("worker_categories", ["user_id", "category_id"],
       [[q(uid), q(c)] for uid in sorted(workers) for c in workers[uid]["cats"]])

w("-- ---------- where each worker takes jobs ----------")
insert("worker_service_areas", ["user_id", "neighborhood_id"],
       [[q(uid), q(n)] for uid in sorted(workers) for n in workers[uid]["areas"]], chunk=100)

w("-- ---------- problems (150) ----------")
rows = []
for p in problems:
    rows.append([q(p["id"]), q(p["customer"]), q(p["cat"]), q(p["nb"]), q(p["address"]), q(p["title"]),
                 q(p["desc"]), q(p["phone"]), q(p["budget"]), q(p["urgency"]), q(p["preferred"]),
                 q(p["status"]), q(p.get("worker")), q(p["created"]), q(p["updated"])])
insert("problems", ["problem_id", "customer_id", "category_id", "neighborhood_id", "address", "title",
                    "description", "contact_phone", "budget", "urgency", "preferred_date", "status",
                    "assigned_worker_id", "created_at", "updated_at"], rows)

w("-- ---------- problem photos (100) ----------")
insert("problem_photos", ["photo_id", "problem_id", "file_path", "sort_order", "uploaded_at"],
       [[q(x["id"]), q(x["problem"]), q(x["path"]), q(x["k"]), q(x["uploaded"])] for x in photos])

w("-- ---------- offers (INSERT trigger adds notifications; they are rebuilt at the end) ----------")
insert("offers", ["offer_id", "problem_id", "worker_id", "price", "message", "initiated_by", "status",
                  "created_at", "updated_at"],
       [[q(o["id"]), q(o["problem"]), q(o["worker"]), q(o["price"]), q(o["message"]), q(o["initiated_by"]),
         q(o["status"]), q(o["created"]), q(o.get("changed", o["created"]))] for o in offers])

w("-- ---------- reviews (100; one per completed job) ----------")
insert("reviews", ["review_id", "problem_id", "worker_id", "customer_id", "rating", "review_text", "created_at"],
       [[q(r["id"]), q(r["problem"]), q(r["worker"]), q(r["customer"]), q(r["rating"]), q(r["text"]),
         q(r["created"])] for r in reviews], chunk=1)   # one by one so the duplicate trigger sees earlier rows

w("-- ---------- messages (100) ----------")
insert("messages", ["message_id", "sender_id", "receiver_id", "problem_id", "content", "is_read", "sent_at"],
       [[q(m["id"]), q(m["sender"]), q(m["receiver"]), q(m["problem"]), q(m["content"]), q(m["read"]),
         q(m["sent"])] for m in messages])

w("-- ---------- saved workers (100) / saved problems (100) ----------")
insert("saved_workers", ["customer_id", "worker_id", "saved_at"], [[q(a), q(b), q(c)] for a, b, c in saved_w_rows])
insert("saved_problems", ["worker_id", "problem_id", "saved_at"], [[q(a), q(b), q(c)] for a, b, c in saved_p_rows])

w("-- ---------- problem views (every offer starts with a view) ----------")
insert("problem_views", ["problem_id", "user_id", "viewed_at"], [[q(a), q(b), q(c)] for a, b, c in views], chunk=200)

w("-- ---------- search log (100) ----------")
insert("search_logs", ["user_id", "keyword", "category_filter", "neighborhood_filter", "searched_at"],
       [[q(a), q(b), q(c), q(d), q(e)] for a, b, c, d, e in searches])

w("-- ---------- chatbot log (50 conversations, 100 messages) ----------")
insert("ai_conversations", ["conversation_id", "user_id", "title", "started_at"],
       [[q(i), q(c["user"]), q(c["title"]), q(c["started"])] for i, c in enumerate(convs, 1)])
insert("ai_messages", ["conversation_id", "sender", "content", "sent_at"],
       [[q(m["conv"]), q(m["sender"]), q(m["content"]), q(m["sent"])] for m in ai_msgs])

w("-- ---------- notifications: replace the ones the triggers just made (wrong timestamps) ----------")
w("DELETE FROM notifications;")
w("ALTER TABLE notifications AUTO_INCREMENT = 1;")
insert("notifications", ["user_id", "type", "message", "is_read", "created_at"],
       [[q(n["user"]), q(n["type"]), q(n["msg"]), q(n["read"]), q(n["when"])] for n in notifs], chunk=200)

w("-- ---------- For You feed for every worker (computed by the DB itself) ----------")
for uid in sorted(workers):
    w(f"CALL sp_generate_recommendations({uid});")
w(f"UPDATE recommendations SET generated_at = {q(NOW)};")

open(sys.argv[1], "w", encoding="utf-8").write("\n".join(out) + "\n")

# side file: review labels for the ML retraining step
import csv
with open(sys.argv[1].replace(".sql", "_review_labels.csv"), "w", newline="", encoding="utf-8") as f:
    cw = csv.writer(f); cw.writerow(["review_id", "rating", "review_text", "labels"])
    for r in reviews: cw.writerow([r["id"], r["rating"], r["text"] or "", "|".join(r["labels"])])

print("users", len(users), "workers", len(workers), "problems", len(problems), "offers", len(offers),
      "reviews", len(reviews), "photos", len(photos), "messages", len(messages), "views", len(views),
      "notifs", len(notifs), "searches", len(searches), "convs", len(convs), "ai_msgs", len(ai_msgs),
      "areas", sum(len(x["areas"]) for x in workers.values()))
from collections import Counter
print(Counter(p["status"] for p in problems))
