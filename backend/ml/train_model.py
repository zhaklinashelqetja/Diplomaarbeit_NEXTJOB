"""
train_model.py — trains the NextJob review analysis models.

Method: TF-IDF (word 1-2 grams) + Logistic Regression
  Model 1: sentiment classifier   (positive / negative / mixed)
  Model 2: category classifier    (multi-label, One-vs-Rest, 10 categories)

Run:    python3 train_model.py
Output: models/sentiment_model.joblib
        models/category_model.joblib
Prints evaluation metrics (hold-out test split) and the most important
words per category — useful for the diploma documentation (explainability).
"""
import csv
import os

import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, f1_score
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MultiLabelBinarizer

DATA = os.path.join(os.path.dirname(__file__), "training_reviews.csv")
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")


def load_data():
    texts, sentiments, labels = [], [], []
    with open(DATA, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            texts.append(row["text"])
            sentiments.append(row["sentiment"])
            labels.append(row["labels"].split("|"))
    return texts, sentiments, labels


def main():
    os.makedirs(MODEL_DIR, exist_ok=True)
    texts, sentiments, labels = load_data()

    X_tr, X_te, s_tr, s_te, l_tr, l_te = train_test_split(
        texts, sentiments, labels, test_size=0.2, random_state=42,
        stratify=sentiments)

    # ---------- Model 1: sentiment ----------
    sent_pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                                  sublinear_tf=True)),
        ("clf", LogisticRegression(max_iter=1000, C=5.0)),
    ])
    sent_pipe.fit(X_tr, s_tr)
    print("=" * 60)
    print("SENTIMENT MODEL (positive / negative / mixed)")
    print(classification_report(s_te, sent_pipe.predict(X_te), digits=3))

    # ---------- Model 2: categories (multi-label) ----------
    mlb = MultiLabelBinarizer()
    Y_tr = mlb.fit_transform(l_tr)
    Y_te = mlb.transform(l_te)

    cat_pipe = Pipeline([
        ("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                                  sublinear_tf=True)),
        ("clf", OneVsRestClassifier(
            LogisticRegression(max_iter=1000, C=5.0))),
    ])
    cat_pipe.fit(X_tr, Y_tr)
    Y_pred = cat_pipe.predict(X_te)
    print("=" * 60)
    print("CATEGORY MODEL (multi-label, 10 categories)")
    print(classification_report(Y_te, Y_pred, target_names=mlb.classes_,
                                digits=3, zero_division=0))
    print(f"micro F1: {f1_score(Y_te, Y_pred, average='micro'):.3f}   "
          f"macro F1: {f1_score(Y_te, Y_pred, average='macro'):.3f}")

    # ---------- explainability: top words per category ----------
    print("=" * 60)
    print("TOP INDICATOR WORDS PER CATEGORY (for the documentation)")
    vec = cat_pipe.named_steps["tfidf"]
    ovr = cat_pipe.named_steps["clf"]
    feats = np.array(vec.get_feature_names_out())
    for cat, est in zip(mlb.classes_, ovr.estimators_):
        top = feats[np.argsort(est.coef_[0])[-6:]][::-1]
        print(f"  {cat:<14} -> {', '.join(top)}")

    joblib.dump(sent_pipe, os.path.join(MODEL_DIR, "sentiment_model.joblib"))
    joblib.dump({"pipeline": cat_pipe, "mlb": mlb},
                os.path.join(MODEL_DIR, "category_model.joblib"))
    print("=" * 60)
    print(f"models saved to {MODEL_DIR}/")


if __name__ == "__main__":
    main()
