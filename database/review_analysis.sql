-- ============================================================
-- NextJob — Review Analysis (Data Science module)
-- Run once against the nextjob database.
-- ============================================================
USE nextjob;

-- one analysis result per review
CREATE TABLE IF NOT EXISTS review_analysis (
    analysis_id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    review_id            INT UNSIGNED NOT NULL UNIQUE,
    sentiment            ENUM('positive','negative','mixed','neutral') NOT NULL,
    sentiment_confidence DECIMAL(5,4) NOT NULL DEFAULT 0,
    model_version        VARCHAR(10)  NOT NULL DEFAULT '1.0',
    analyzed_at          TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                                      ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_ra_review FOREIGN KEY (review_id)
        REFERENCES reviews(review_id) ON DELETE CASCADE,
    INDEX idx_ra_sentiment (sentiment)
) ENGINE=InnoDB;

-- detected categories per analysis (0..n rows)
CREATE TABLE IF NOT EXISTS review_analysis_categories (
    id          INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    analysis_id INT UNSIGNED NOT NULL,
    category    ENUM('price_fair','punctual','high_quality','fast_response',
                     'friendly','overpriced','late','poor_quality',
                     'slow_response','rude') NOT NULL,
    polarity    ENUM('positive','negative') NOT NULL,
    score       DECIMAL(5,4) NOT NULL,
    CONSTRAINT fk_rac_analysis FOREIGN KEY (analysis_id)
        REFERENCES review_analysis(analysis_id) ON DELETE CASCADE,
    UNIQUE KEY uq_analysis_category (analysis_id, category),
    INDEX idx_rac_category (category)
) ENGINE=InnoDB;

-- ------------------------------------------------------------
-- Aggregation views
-- ------------------------------------------------------------

-- per-worker category profile: how often each category appears
-- in the worker's reviews + average model confidence
CREATE OR REPLACE VIEW v_worker_category_scores AS
SELECT
    r.worker_id,
    rac.category,
    rac.polarity,
    COUNT(*)                    AS mentions,
    ROUND(AVG(rac.score), 3)    AS avg_score,
    ROUND(COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM reviews r2 WHERE r2.worker_id = r.worker_id),
        1)                      AS pct_of_reviews
FROM reviews r
JOIN review_analysis ra  ON ra.review_id  = r.review_id
JOIN review_analysis_categories rac ON rac.analysis_id = ra.analysis_id
GROUP BY r.worker_id, rac.category, rac.polarity;

-- per-worker sentiment breakdown
CREATE OR REPLACE VIEW v_worker_sentiment AS
SELECT
    r.worker_id,
    COUNT(*)                                              AS analyzed_reviews,
    SUM(ra.sentiment = 'positive')                        AS positive_cnt,
    SUM(ra.sentiment = 'negative')                        AS negative_cnt,
    SUM(ra.sentiment = 'mixed')                           AS mixed_cnt,
    ROUND(SUM(ra.sentiment = 'positive') * 100.0 / COUNT(*), 1)
                                                          AS positive_pct
FROM reviews r
JOIN review_analysis ra ON ra.review_id = r.review_id
GROUP BY r.worker_id;

-- platform-wide category demand/complaint statistics
CREATE OR REPLACE VIEW v_platform_category_stats AS
SELECT
    rac.category,
    rac.polarity,
    COUNT(*)                 AS total_mentions,
    ROUND(AVG(rac.score), 3) AS avg_score
FROM review_analysis_categories rac
GROUP BY rac.category, rac.polarity
ORDER BY total_mentions DESC;
