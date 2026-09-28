"""
generate_data.py — creates a synthetic labeled review dataset for NextJob.

10 categories (5 positive / 5 negative), multi-label:
  POSITIVE: price_fair, punctual, high_quality, fast_response, friendly
  NEGATIVE: overpriced, late, poor_quality, slow_response, rude

Output: training_reviews.csv  (columns: text, sentiment, labels)
        labels = pipe-separated category list, e.g. "punctual|high_quality"
"""
import csv
import random

random.seed(42)

CATEGORIES = {
    # ---------------- POSITIVE ----------------
    "price_fair": [
        "good price",
        "cheap and good",
        "the price is right",
        "fair price for good work",
        "the price was very fair",
        "great value for money",
        "charged exactly what was quoted, no surprises",
        "very reasonable price for the work done",
        "affordable and honest pricing",
        "the cost was lower than I expected",
        "fair quote and stuck to it",
        "didn't overcharge me at all, honest guy",
        "best price I could find for this job",
        "transparent pricing from the start",
    ],
    "punctual": [
        "on time",
        "right on time",
        "always punctual",
        "arrived exactly on time",
        "he was punctual and ready to work",
        "showed up right when he said he would",
        "came even a few minutes early",
        "always on time on both days",
        "very punctual, respected my schedule",
        "was there at 8 sharp as agreed",
        "finished the job within the promised time",
        "kept to the agreed schedule perfectly",
    ],
    "high_quality": [
        "the work quality is really good",
        "solid quality work",
        "his work is really good",
        "fixed everything perfectly",
        "solid work",
        "quality is top",
        "great quality work",
        "did a quality job",
        "excellent quality",
        "amazing work, really well done",
        "the work is very good",
        "good quality and durable",
        "perfect job",
        "outstanding work on my bathroom",
        "the quality of the work is excellent",
        "flawless workmanship, everything works perfectly",
        "very professional result, looks amazing",
        "top quality job, no issues since",
        "the repair was done perfectly",
        "clean and precise work, real craftsmanship",
        "everything was installed properly and works great",
        "attention to detail was impressive",
        "solid work that will last for years",
        "left everything clean and tidy after finishing",
    ],
    "fast_response": [
        "quick response",
        "fast reply",
        "responds fast",
        "very responsive",
        "replied to my request within minutes",
        "very quick to respond to my messages",
        "answered immediately and came the same day",
        "got back to me right away",
        "super fast communication throughout",
        "responded quickly and scheduled the visit fast",
        "instant reply when I contacted him",
        "same day service, incredibly fast",
    ],
    "friendly": [
        "very friendly the whole time",
        "nice guy",
        "nice and friendly",
        "super friendly",
        "kind person",
        "polite and helpful",
        "very friendly and polite",
        "such a kind and respectful person",
        "explained everything patiently and nicely",
        "pleasant to deal with, great attitude",
        "courteous and professional in every way",
        "made me feel comfortable, very nice guy",
        "friendly, honest and easy to talk to",
        "treated my home with respect, lovely person",
    ],
    # ---------------- NEGATIVE ----------------
    "overpriced": [
        "too expensive",
        "way too expensive for what he did",
        "very expensive",
        "the bill was huge",
        "expensive and not worth it",
        "way too expensive for what he did",
        "charged much more than the original quote",
        "the price was a complete rip off",
        "added hidden costs at the end",
        "overpriced for such a simple job",
        "demanded extra money for no reason",
        "final bill was double the estimate",
        "not worth the money at all",
        "his prices are absurdly high",
    ],
    "late": [
        "came very late",
        "he was late",
        "arrived late without any excuse",
        "hours late",
        "showed up two hours late",
        "was late both days without warning",
        "never arrived at the agreed time",
        "kept me waiting all morning",
        "postponed twice and then came late anyway",
        "did not respect the schedule at all",
        "the job took twice as long as promised",
        "missed the appointment completely",
        "always late, wasted my whole day",
    ],
    "poor_quality": [
        "left a small mess",
        "sloppy work",
        "bad quality",
        "bad work",
        "the work was awful",
        "low quality job",
        "did a horrible job",
        "the work quality was terrible",
        "sloppy job, it broke again after a week",
        "left a mess and the repair failed",
        "very unprofessional result, had to redo it",
        "the installation was done wrong",
        "poor workmanship, crooked and leaking",
        "cheap materials and careless work",
        "damaged my wall while working",
        "the problem came back two days later",
        "had to hire someone else to fix his mistakes",
    ],
    "slow_response": [
        "response time could be faster",
        "communication was slow",
        "took long to get back to me",
        "slow to reply",
        "takes forever to answer",
        "not responsive at all",
        "took days to answer my messages",
        "never replies, impossible to reach",
        "ignored my calls for a week",
        "extremely slow communication",
        "had to chase him constantly for updates",
        "stopped responding after the first visit",
        "waited forever just to get a quote",
        "communication was painfully slow",
    ],
    "rude": [
        "quite rude when I asked questions",
        "got rude with me",
        "he was very rude",
        "so rude to me",
        "rude and unprofessional behavior",
        "had a bad attitude",
        "was really rude on the phone",
        "such a rude person",
        "very rude and dismissive",
        "was arrogant and talked down to me",
        "unfriendly attitude the whole time",
        "got aggressive when I asked questions",
        "disrespectful towards me and my home",
        "impolite and impatient with everything",
        "yelled at me when I pointed out a mistake",
        "zero manners, very unpleasant person",
    ],
}

POSITIVE = ["price_fair", "punctual", "high_quality", "fast_response", "friendly"]
NEGATIVE = ["overpriced", "late", "poor_quality", "slow_response", "rude"]

OPENERS_POS = ["", "Highly recommend. ", "Great experience. ", "Very satisfied. ",
               "Would hire again. ", "Excellent worker. ", "Really happy with this. "]
OPENERS_NEG = ["", "Avoid this worker. ", "Very disappointed. ", "Bad experience. ",
               "Would not recommend. ", "Terrible service. ", "Not happy at all. "]
CONNECTORS = [" and ", ". Also ", ", plus ", ". On top of that ", " — "]
MIXED_TURNS = [". However ", ". Unfortunately ", ", but ", ". The downside: ",
               ". Sadly "]


def make_review(cats):
    """Compose one review text from 1-3 category phrase snippets."""
    pos = [c for c in cats if c in POSITIVE]
    neg = [c for c in cats if c in NEGATIVE]
    parts_pos = [random.choice(CATEGORIES[c]) for c in pos]
    parts_neg = [random.choice(CATEGORIES[c]) for c in neg]

    def join(parts):
        text = parts[0]
        for p in parts[1:]:
            text += random.choice(CONNECTORS) + p
        return text

    if pos and neg:  # mixed review
        text = random.choice(OPENERS_POS) + join(parts_pos) \
             + random.choice(MIXED_TURNS) + join(parts_neg)
        sentiment = "mixed"
    elif pos:
        text = random.choice(OPENERS_POS) + join(parts_pos)
        sentiment = "positive"
    else:
        text = random.choice(OPENERS_NEG) + join(parts_neg)
        sentiment = "negative"

    text = text[0].upper() + text[1:]
    if not text.endswith("."):
        text += "."
    return text, sentiment


def main(n_samples=800, out="training_reviews.csv"):
    rows = []
    all_cats = list(CATEGORIES)
    for _ in range(n_samples):
        r = random.random()
        if r < 0.40:                       # single category
            cats = random.sample(all_cats, 1)
        elif r < 0.75:                     # two, same polarity
            pool = POSITIVE if random.random() < 0.5 else NEGATIVE
            cats = random.sample(pool, 2)
        elif r < 0.90:                     # three, same polarity
            pool = POSITIVE if random.random() < 0.5 else NEGATIVE
            cats = random.sample(pool, 3)
        else:                              # mixed polarity
            cats = random.sample(POSITIVE, 1) + random.sample(NEGATIVE, 1)
        text, sentiment = make_review(cats)
        rows.append((text, sentiment, "|".join(sorted(cats))))

    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["text", "sentiment", "labels"])
        w.writerows(rows)
    print(f"wrote {len(rows)} samples to {out}")


if __name__ == "__main__":
    main()
