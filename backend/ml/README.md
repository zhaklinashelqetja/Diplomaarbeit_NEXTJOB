# NextJob — Review Analysis (Data-Science Module)

Semantisches Bewertungssystem: TF-IDF + Logistic Regression, trained on a
synthetic labeled dataset. Detects overall sentiment (positive / negative /
mixed) and 10 categories per review:

| Positive       | Negative      |
|----------------|---------------|
| price_fair     | overpriced    |
| punctual       | late          |
| high_quality   | poor_quality  |
| fast_response  | slow_response |
| friendly       | rude          |

Test metrics (hold-out 20%): sentiment accuracy ~0.94, category micro-F1 ~0.94.

## Contents
```
ml/
  generate_data.py      builds training_reviews.csv (800 labeled samples)
  train_model.py        trains + evaluates both models, saves to ml/models/
  analyzer.py           runtime analysis: analyze_review(text) -> dict
  batch_analyze.py      analyze all unanalyzed reviews from the command line
  training_reviews.csv  the dataset
  models/               trained joblib models
routes/analysis_routes.py   Flask blueprint /api/analysis/* (registered in app.py)
database/02_review_analysis.sql   2 tables + 3 views
```

The models were trained with scikit-learn 1.8.0, so requirements.txt pins
that version. After retraining, the pin can be raised to the new version.

## API
```
POST /api/analysis/preview          {"text": "..."}  -> analysis, nothing stored (login)
GET  /api/analysis/reviews/<id>     stored result (login)
GET  /api/analysis/workers/<id>     strengths/weaknesses + sentiment (public)
POST /api/analysis/reviews/<id>     analyze + store one review (admin)
POST /api/analysis/run              analyze all unanalyzed reviews (admin)
```

## Nice DataGrip demo queries
```sql
SELECT * FROM v_worker_sentiment;
SELECT * FROM v_worker_category_scores WHERE worker_id = 1;
SELECT * FROM v_platform_category_stats;
```

## Retraining
```bash
cd ml && python3 generate_data.py && python3 train_model.py
```
`train_model.py` also prints the top indicator words per category —
use that in the documentation (explainability of the model).

## Known limitation (for the docs)
Trained on synthetic English data; sentences whose polarity depends on
context (e.g. "Poor quality." as standalone fragment after positive words)
can be misclassified. Threshold for category detection: 0.5
(ml/analyzer.py -> CATEGORY_THRESHOLD).
