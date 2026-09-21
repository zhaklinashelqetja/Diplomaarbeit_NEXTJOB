"""
analyzer.py — runtime review analysis for the NextJob API.

Usage:
    from ml.analyzer import analyze_review
    result = analyze_review("Arrived on time but way too expensive.")

Returns:
    {
      "sentiment": "mixed",              # positive | negative | mixed
      "sentiment_confidence": 0.94,      # probability of predicted class
      "categories": [
        {"category": "punctual",   "polarity": "positive", "score": 0.91},
        {"category": "overpriced", "polarity": "negative", "score": 0.88}
      ],
      "model_version": "1.0"
    }

Models are loaded once at import time (fast inference, no reload per request).
"""
import os

import joblib

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
MODEL_VERSION = "1.0"

# categories with polarity — must match generate_data.py
POSITIVE = {"price_fair", "punctual", "high_quality", "fast_response", "friendly"}
NEGATIVE = {"overpriced", "late", "poor_quality", "slow_response", "rude"}

# probability threshold: a category counts as detected above this value
CATEGORY_THRESHOLD = 0.5

_sentiment = joblib.load(os.path.join(MODEL_DIR, "sentiment_model.joblib"))
_cat_bundle = joblib.load(os.path.join(MODEL_DIR, "category_model.joblib"))
_cat_pipe = _cat_bundle["pipeline"]
_mlb = _cat_bundle["mlb"]


def analyze_review(text: str) -> dict:
    text = (text or "").strip()
    if not text:
        return {"sentiment": "neutral", "sentiment_confidence": 0.0,
                "categories": [], "model_version": MODEL_VERSION}

    # sentiment
    probs = _sentiment.predict_proba([text])[0]
    idx = probs.argmax()
    sentiment = _sentiment.classes_[idx]
    confidence = float(round(probs[idx], 4))

    # categories (multi-label probabilities)
    cat_probs = _cat_pipe.predict_proba([text])[0]
    categories = []
    for cat, p in zip(_mlb.classes_, cat_probs):
        if p >= CATEGORY_THRESHOLD:
            categories.append({
                "category": cat,
                "polarity": "positive" if cat in POSITIVE else "negative",
                "score": float(round(p, 4)),
            })
    categories.sort(key=lambda c: c["score"], reverse=True)

    # consistency: derive sentiment from categories if the two models disagree
    has_pos = any(c["polarity"] == "positive" for c in categories)
    has_neg = any(c["polarity"] == "negative" for c in categories)
    if has_pos and has_neg:
        sentiment = "mixed"
    elif has_pos and sentiment == "negative":
        sentiment = "positive"
    elif has_neg and sentiment == "positive":
        sentiment = "negative"

    return {"sentiment": sentiment,
            "sentiment_confidence": confidence,
            "categories": categories,
            "model_version": MODEL_VERSION}


if __name__ == "__main__":  # quick manual test
    import json
    samples = [
        "He arrived exactly on time and the price was very fair.",
        "Terrible experience, showed up two hours late and was very rude.",
        "Great quality work, but way too expensive for what he did.",
        "Replied within minutes and fixed everything the same day.",
    ]
    for s in samples:
        print(s)
        print(json.dumps(analyze_review(s), indent=2), "\n")
