-- ============================================================
-- NextJob — Handyman Marketplace (Diploma Project)
-- Dialect: MySQL 8.x  |  Run in DataGrip top to bottom
--
-- Concept:
--   * One account can be customer AND worker.
--     A user becomes a worker by having a row in worker_profiles.
--   * Customers post PROBLEMS (with photos, category, location,
--     contact number). Workers make OFFERS with a price (paid
--     per job, no hourly rate). Customers can also contact a
--     worker directly -> the worker then sends an offer
--     (initiated_by = 'customer').
--   * Reviews go to WORKERS only, one per completed problem.
--   * recommendations table = cache for the future Python
--     "For You" matching algorithm.
-- ============================================================

DROP DATABASE IF EXISTS nextjob;
CREATE DATABASE nextjob CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE nextjob;

-- ============================================================
-- 1. TABLES
-- ============================================================

-- ---------- users (every account: customer, worker or both) ----------
CREATE TABLE users (
    user_id       INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    is_admin      BOOLEAN      NOT NULL DEFAULT FALSE,
    first_name    VARCHAR(60)  NOT NULL,
    last_name     VARCHAR(60)  NOT NULL,
    email         VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    phone         VARCHAR(30),
    location      VARCHAR(100),
    avatar_path   VARCHAR(255),
    is_active     BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
                               ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_users_location (location)
) ENGINE = InnoDB;

-- ---------- categories (fixed trade vocabulary) ----------
CREATE TABLE categories (
    category_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(60) NOT NULL UNIQUE,
    icon        VARCHAR(60)
) ENGINE = InnoDB;

-- ---------- worker_profiles (user becomes a worker) ----------
CREATE TABLE worker_profiles (
    user_id          INT UNSIGNED PRIMARY KEY,
    headline         VARCHAR(150),
    bio              TEXT,
    years_experience TINYINT UNSIGNED NOT NULL DEFAULT 0,
    service_area     VARCHAR(100),          -- where the worker operates
    is_available     BOOLEAN NOT NULL DEFAULT TRUE,
    created_at       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_wp_user FOREIGN KEY (user_id) REFERENCES users (user_id)
        ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- worker_categories (M:N — a worker's trades) ----------
CREATE TABLE worker_categories (
    user_id     INT UNSIGNED NOT NULL,
    category_id INT UNSIGNED NOT NULL,
    PRIMARY KEY (user_id, category_id),
    CONSTRAINT fk_wc_worker FOREIGN KEY (user_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_wc_cat FOREIGN KEY (category_id)
        REFERENCES categories (category_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- problems (posted by customers) ----------
CREATE TABLE problems (
    problem_id         INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    customer_id        INT UNSIGNED NOT NULL,
    category_id        INT UNSIGNED NOT NULL,   -- type of worker needed
    title              VARCHAR(150) NOT NULL,
    description        TEXT NOT NULL,
    location           VARCHAR(100) NOT NULL,
    contact_phone      VARCHAR(30)  NOT NULL,
    budget             DECIMAL(10,2),           -- optional customer budget
    urgency            ENUM('low','normal','high','emergency')
                       NOT NULL DEFAULT 'normal',
    preferred_date     DATE,
    status             ENUM('open','assigned','in_progress','completed','cancelled')
                       NOT NULL DEFAULT 'open',
    assigned_worker_id INT UNSIGNED NULL,       -- set when an offer is accepted
    created_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                       ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_prob_customer FOREIGN KEY (customer_id)
        REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_prob_category FOREIGN KEY (category_id)
        REFERENCES categories (category_id),
    CONSTRAINT fk_prob_worker FOREIGN KEY (assigned_worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE SET NULL,
    INDEX idx_prob_status (status),
    INDEX idx_prob_location (location),
    INDEX idx_prob_category (category_id)
) ENGINE = InnoDB;

-- ---------- problem_photos (multiple photos per problem) ----------
CREATE TABLE problem_photos (
    photo_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    problem_id INT UNSIGNED NOT NULL,
    file_path  VARCHAR(255) NOT NULL,
    sort_order TINYINT UNSIGNED NOT NULL DEFAULT 0,
    uploaded_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pp_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- offers (worker bids on a problem, price per job) ----------
CREATE TABLE offers (
    offer_id     INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    problem_id   INT UNSIGNED NOT NULL,
    worker_id    INT UNSIGNED NOT NULL,
    price        DECIMAL(10,2) NOT NULL,   -- fixed price for the whole job
    message      TEXT,
    initiated_by ENUM('worker','customer') NOT NULL DEFAULT 'worker',
    status       ENUM('pending','accepted','rejected','withdrawn')
                 NOT NULL DEFAULT 'pending',
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
                 ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_off_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE,
    CONSTRAINT fk_off_worker FOREIGN KEY (worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE,
    CONSTRAINT uq_offer UNIQUE (problem_id, worker_id),
    CONSTRAINT chk_offer_price CHECK (price > 0),
    INDEX idx_off_status (status)
) ENGINE = InnoDB;

-- ---------- reviews (customer -> worker, one per completed problem) ----------
CREATE TABLE reviews (
    review_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    problem_id  INT UNSIGNED NOT NULL UNIQUE,   -- max one review per job
    worker_id   INT UNSIGNED NOT NULL,
    customer_id INT UNSIGNED NOT NULL,
    rating      TINYINT UNSIGNED NOT NULL,
    review_text TEXT,
    is_flagged  BOOLEAN NOT NULL DEFAULT FALSE,
    flag_reason VARCHAR(120),
    created_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_rev_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE,
    CONSTRAINT fk_rev_worker FOREIGN KEY (worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_rev_customer FOREIGN KEY (customer_id)
        REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT chk_rating CHECK (rating BETWEEN 1 AND 5)
) ENGINE = InnoDB;

-- ---------- messages (direct contact customer <-> worker) ----------
CREATE TABLE messages (
    message_id  BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    sender_id   INT UNSIGNED NOT NULL,
    receiver_id INT UNSIGNED NOT NULL,
    problem_id  INT UNSIGNED NULL,   -- optional: chat about a specific problem
    content     TEXT NOT NULL,
    is_read     BOOLEAN NOT NULL DEFAULT FALSE,
    sent_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_msg_sender   FOREIGN KEY (sender_id)
        REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_msg_receiver FOREIGN KEY (receiver_id)
        REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_msg_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE SET NULL
) ENGINE = InnoDB;

-- ---------- notifications ----------
CREATE TABLE notifications (
    notification_id BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    type            ENUM('offer','job','message','review','job_match','system')
                    NOT NULL DEFAULT 'system',
    message         VARCHAR(255) NOT NULL,
    is_read         BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notif_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- saved_workers (customer bookmarks a worker) ----------
CREATE TABLE saved_workers (
    customer_id INT UNSIGNED NOT NULL,
    worker_id   INT UNSIGNED NOT NULL,
    saved_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (customer_id, worker_id),
    CONSTRAINT fk_sw_customer FOREIGN KEY (customer_id)
        REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_sw_worker FOREIGN KEY (worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- saved_problems (worker bookmarks a problem) ----------
CREATE TABLE saved_problems (
    worker_id  INT UNSIGNED NOT NULL,
    problem_id INT UNSIGNED NOT NULL,
    saved_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (worker_id, problem_id),
    CONSTRAINT fk_sp_worker FOREIGN KEY (worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_sp_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- problem_views (statistics + For You data) ----------
CREATE TABLE problem_views (
    view_id    BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    problem_id INT UNSIGNED NOT NULL,
    user_id    INT UNSIGNED NULL,
    viewed_at  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_pv_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE,
    CONSTRAINT fk_pv_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON DELETE SET NULL,
    INDEX idx_pv_problem (problem_id)
) ENGINE = InnoDB;

-- ---------- search_logs (statistics) ----------
CREATE TABLE search_logs (
    search_id       BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NULL,
    keyword         VARCHAR(120),
    category_filter INT UNSIGNED NULL,
    location_filter VARCHAR(100),
    searched_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_sl_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON DELETE SET NULL,
    CONSTRAINT fk_sl_cat FOREIGN KEY (category_filter)
        REFERENCES categories (category_id) ON DELETE SET NULL,
    INDEX idx_sl_keyword (keyword)
) ENGINE = InnoDB;

-- ---------- ai_conversations / ai_messages (assistant feature) ----------
CREATE TABLE ai_conversations (
    conversation_id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id         INT UNSIGNED NOT NULL,
    title           VARCHAR(150) NOT NULL DEFAULT 'New conversation',
    started_at      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_ac_user FOREIGN KEY (user_id)
        REFERENCES users (user_id) ON DELETE CASCADE
) ENGINE = InnoDB;

CREATE TABLE ai_messages (
    ai_message_id   BIGINT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    conversation_id INT UNSIGNED NOT NULL,
    sender          ENUM('user','assistant') NOT NULL,
    content         TEXT NOT NULL,
    sent_at         DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_am_conv FOREIGN KEY (conversation_id)
        REFERENCES ai_conversations (conversation_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ---------- recommendations (For You cache — worker <- problem) ----------
CREATE TABLE recommendations (
    worker_id    INT UNSIGNED NOT NULL,
    problem_id   INT UNSIGNED NOT NULL,
    score        DECIMAL(5,2) NOT NULL,
    generated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (worker_id, problem_id),
    CONSTRAINT fk_rec_worker FOREIGN KEY (worker_id)
        REFERENCES worker_profiles (user_id) ON DELETE CASCADE,
    CONSTRAINT fk_rec_problem FOREIGN KEY (problem_id)
        REFERENCES problems (problem_id) ON DELETE CASCADE
) ENGINE = InnoDB;

-- ============================================================
-- 2. SEED DATA — fixed trade categories (do NOT mock this)
-- ============================================================
INSERT INTO categories (name, icon) VALUES
('Plumber','pipe'), ('Electrician','bolt'), ('Painter','brush'),
('Carpenter','hammer'), ('Mason','brick'), ('Roofer','roof'),
('HVAC Technician','fan'), ('Gardener','leaf'), ('Cleaner','spray'),
('Locksmith','key'), ('Tiler','grid'), ('Welder','flame'),
('Appliance Repair','wrench'), ('Moving & Transport','truck'),
('General Handyman','toolbox');

-- ============================================================
-- 3. FUNCTION — match score worker <-> problem (For You feed)
--    Simple SQL baseline; the smarter Python algorithm will
--    later overwrite the recommendations table with its scores.
--    Category match = 60 | Location match = 30 | Available = 10
-- ============================================================
DELIMITER //
CREATE FUNCTION fn_match_score(p_worker_id INT UNSIGNED, p_problem_id INT UNSIGNED)
RETURNS DECIMAL(5,2)
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE v_score        DECIMAL(5,2) DEFAULT 0;
    DECLARE v_prob_cat     INT UNSIGNED;
    DECLARE v_prob_loc     VARCHAR(100);
    DECLARE v_worker_area  VARCHAR(100);
    DECLARE v_available    BOOLEAN;

    SELECT category_id, location INTO v_prob_cat, v_prob_loc
    FROM problems WHERE problem_id = p_problem_id;

    IF v_prob_cat IS NULL THEN
        RETURN 0.00;
    END IF;

    SELECT service_area, is_available INTO v_worker_area, v_available
    FROM worker_profiles WHERE user_id = p_worker_id;

    -- category match (mandatory for any score)
    IF EXISTS (SELECT 1 FROM worker_categories
               WHERE user_id = p_worker_id AND category_id = v_prob_cat) THEN
        SET v_score = 60;
    ELSE
        RETURN 0.00;
    END IF;

    -- location match
    IF v_worker_area IS NOT NULL AND v_prob_loc IS NOT NULL
       AND LOWER(v_worker_area) = LOWER(v_prob_loc) THEN
        SET v_score = v_score + 30;
    END IF;

    -- availability bonus
    IF v_available THEN
        SET v_score = v_score + 10;
    END IF;

    RETURN v_score;
END //
DELIMITER ;

-- ============================================================
-- 4. STORED PROCEDURES
-- ============================================================

-- Worker makes an offer on a problem (all checks in one place)
DELIMITER //
CREATE PROCEDURE sp_make_offer(
    IN p_worker_id  INT UNSIGNED,
    IN p_problem_id INT UNSIGNED,
    IN p_price      DECIMAL(10,2),
    IN p_message    TEXT,
    IN p_initiated_by VARCHAR(10)   -- 'worker' or 'customer'
)
BEGIN
    DECLARE v_status      VARCHAR(15);
    DECLARE v_customer_id INT UNSIGNED;

    SELECT status, customer_id INTO v_status, v_customer_id
    FROM problems WHERE problem_id = p_problem_id;

    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem does not exist';
    ELSEIF v_status <> 'open' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem is not open';
    ELSEIF NOT EXISTS (SELECT 1 FROM worker_profiles
                       WHERE user_id = p_worker_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'User is not a worker';
    ELSEIF v_customer_id = p_worker_id THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Cannot offer on own problem';
    ELSEIF EXISTS (SELECT 1 FROM offers
                   WHERE problem_id = p_problem_id
                     AND worker_id = p_worker_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Offer already exists';
    ELSE
        INSERT INTO offers (problem_id, worker_id, price, message, initiated_by)
        VALUES (p_problem_id, p_worker_id, p_price, p_message,
                IF(p_initiated_by = 'customer', 'customer', 'worker'));
    END IF;
END //
DELIMITER ;

-- Customer accepts one offer -> rejects the rest, assigns the worker
DELIMITER //
CREATE PROCEDURE sp_accept_offer(IN p_offer_id INT UNSIGNED)
BEGIN
    DECLARE v_problem_id INT UNSIGNED;
    DECLARE v_worker_id  INT UNSIGNED;
    DECLARE v_off_status VARCHAR(10);
    DECLARE v_prob_status VARCHAR(15);

    SELECT o.problem_id, o.worker_id, o.status, p.status
    INTO v_problem_id, v_worker_id, v_off_status, v_prob_status
    FROM offers o
    JOIN problems p ON p.problem_id = o.problem_id
    WHERE o.offer_id = p_offer_id;

    IF v_problem_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Offer does not exist';
    ELSEIF v_off_status <> 'pending' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Offer is not pending';
    ELSEIF v_prob_status <> 'open' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem is not open';
    ELSE
        UPDATE offers SET status = 'accepted'
        WHERE offer_id = p_offer_id;

        UPDATE offers SET status = 'rejected'
        WHERE problem_id = v_problem_id
          AND offer_id <> p_offer_id
          AND status = 'pending';

        UPDATE problems
        SET status = 'assigned', assigned_worker_id = v_worker_id
        WHERE problem_id = v_problem_id;
    END IF;
END //
DELIMITER ;

-- Mark a job as completed (only from assigned/in_progress)
DELIMITER //
CREATE PROCEDURE sp_complete_problem(IN p_problem_id INT UNSIGNED)
BEGIN
    DECLARE v_status VARCHAR(15);

    SELECT status INTO v_status FROM problems WHERE problem_id = p_problem_id;

    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem does not exist';
    ELSEIF v_status NOT IN ('assigned','in_progress') THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem is not in progress';
    ELSE
        UPDATE problems SET status = 'completed'
        WHERE problem_id = p_problem_id;
    END IF;
END //
DELIMITER ;

-- Customer leaves a review — only for their own completed job
DELIMITER //
CREATE PROCEDURE sp_leave_review(
    IN p_problem_id  INT UNSIGNED,
    IN p_customer_id INT UNSIGNED,
    IN p_rating      TINYINT UNSIGNED,
    IN p_text        TEXT
)
BEGIN
    DECLARE v_status      VARCHAR(15);
    DECLARE v_customer_id INT UNSIGNED;
    DECLARE v_worker_id   INT UNSIGNED;

    SELECT status, customer_id, assigned_worker_id
    INTO v_status, v_customer_id, v_worker_id
    FROM problems WHERE problem_id = p_problem_id;

    IF v_status IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Problem does not exist';
    ELSEIF v_status <> 'completed' THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Job is not completed yet';
    ELSEIF v_customer_id <> p_customer_id THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Not your problem to review';
    ELSEIF v_worker_id IS NULL THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'No worker was assigned';
    ELSEIF EXISTS (SELECT 1 FROM reviews WHERE problem_id = p_problem_id) THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Job already reviewed';
    ELSE
        INSERT INTO reviews (problem_id, worker_id, customer_id, rating, review_text)
        VALUES (p_problem_id, v_worker_id, p_customer_id, p_rating, p_text);
    END IF;
END //
DELIMITER ;

-- Fake review detection: flags suspicious reviews, never deletes
DELIMITER //
CREATE PROCEDURE sp_detect_fake_reviews()
BEGIN
    -- Rule 1: identical review text appearing more than once
    UPDATE reviews r
    JOIN (
        SELECT review_text
        FROM reviews
        WHERE review_text IS NOT NULL AND review_text <> ''
        GROUP BY review_text
        HAVING COUNT(*) > 1
    ) dup ON r.review_text = dup.review_text
    SET r.is_flagged = TRUE,
        r.flag_reason = 'Duplicate text';

    -- Rule 2: same customer reviewing the same worker 3+ times
    --         (allowed in general — repeat jobs — but 3+ is suspicious)
    UPDATE reviews r
    JOIN (
        SELECT customer_id, worker_id
        FROM reviews
        GROUP BY customer_id, worker_id
        HAVING COUNT(*) >= 3
    ) multi ON r.customer_id = multi.customer_id
           AND r.worker_id   = multi.worker_id
    SET r.is_flagged = TRUE,
        r.flag_reason = 'Many reviews same worker';

    -- Rule 3: burst — customer posted 3+ reviews within one hour
    UPDATE reviews r
    JOIN (
        SELECT r1.review_id
        FROM reviews r1
        JOIN reviews r2 ON r1.customer_id = r2.customer_id
                       AND r1.review_id <> r2.review_id
                       AND ABS(TIMESTAMPDIFF(MINUTE, r1.created_at,
                                                     r2.created_at)) <= 60
        GROUP BY r1.review_id
        HAVING COUNT(*) >= 2
    ) burst ON r.review_id = burst.review_id
    SET r.is_flagged = TRUE,
        r.flag_reason = 'Review burst';
END //
DELIMITER ;

-- Regenerate the For You feed for one worker (top 20 open problems)
DELIMITER //
CREATE PROCEDURE sp_generate_recommendations(IN p_worker_id INT UNSIGNED)
BEGIN
    DELETE FROM recommendations WHERE worker_id = p_worker_id;

    INSERT INTO recommendations (worker_id, problem_id, score)
    SELECT p_worker_id, t.problem_id, t.score
    FROM (
        SELECT pr.problem_id,
               fn_match_score(p_worker_id, pr.problem_id) AS score
        FROM problems pr
        WHERE pr.status = 'open'
    ) t
    WHERE t.score > 0
    ORDER BY t.score DESC
    LIMIT 20;
END //
DELIMITER ;

-- ============================================================
-- 5. TRIGGERS
-- ============================================================

-- New offer -> notify the customer who posted the problem
DELIMITER //
CREATE TRIGGER trg_offer_notify
AFTER INSERT ON offers
FOR EACH ROW
BEGIN
    INSERT INTO notifications (user_id, type, message)
    SELECT p.customer_id, 'offer',
           CONCAT('New offer (', NEW.price, ') on your problem #', NEW.problem_id)
    FROM problems p
    WHERE p.problem_id = NEW.problem_id;
END //
DELIMITER ;

-- Offer status change -> notify the worker
DELIMITER //
CREATE TRIGGER trg_offer_status
AFTER UPDATE ON offers
FOR EACH ROW
BEGIN
    IF NEW.status <> OLD.status THEN
        INSERT INTO notifications (user_id, type, message)
        VALUES (NEW.worker_id, 'offer',
                CONCAT('Your offer on problem #', NEW.problem_id,
                       ' is now: ', NEW.status));
    END IF;
END //
DELIMITER ;

-- Problem status change -> notify both sides where relevant
DELIMITER //
CREATE TRIGGER trg_problem_status
AFTER UPDATE ON problems
FOR EACH ROW
BEGIN
    IF NEW.status <> OLD.status THEN
        -- worker gets informed about status of the assigned job
        IF NEW.assigned_worker_id IS NOT NULL THEN
            INSERT INTO notifications (user_id, type, message)
            VALUES (NEW.assigned_worker_id, 'job',
                    CONCAT('Job #', NEW.problem_id, ' is now: ', NEW.status));
        END IF;
        -- after completion the customer is reminded to review
        IF NEW.status = 'completed' THEN
            INSERT INTO notifications (user_id, type, message)
            VALUES (NEW.customer_id, 'review',
                    CONCAT('Job #', NEW.problem_id,
                           ' completed — leave a review for the worker!'));
        END IF;
    END IF;
END //
DELIMITER ;

-- New review -> notify the worker + instant duplicate-text flag
DELIMITER //
CREATE TRIGGER trg_review_duplicate
BEFORE INSERT ON reviews
FOR EACH ROW
BEGIN
    IF NEW.review_text IS NOT NULL AND NEW.review_text <> '' AND EXISTS (
        SELECT 1 FROM reviews
        WHERE review_text = NEW.review_text
    ) THEN
        SET NEW.is_flagged = TRUE;
        SET NEW.flag_reason = 'Duplicate text';
    END IF;
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_review_notify
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
    INSERT INTO notifications (user_id, type, message)
    VALUES (NEW.worker_id, 'review',
            CONCAT('You received a ', NEW.rating, '-star review'));
END //
DELIMITER ;

-- ============================================================
-- 6. VIEWS — statistics + worker search
-- ============================================================

-- Worker directory: quality (rating), price (avg accepted offer),
-- time (avg response hours) — this powers "find workers by
-- price / time / quality"
CREATE VIEW v_worker_search AS
SELECT wp.user_id                                    AS worker_id,
       CONCAT(u.first_name, ' ', u.last_name)        AS full_name,
       wp.headline,
       wp.service_area,
       wp.years_experience,
       wp.is_available,
       COUNT(DISTINCT CASE WHEN r.is_flagged = FALSE
                           THEN r.review_id END)     AS review_count,
       ROUND(AVG(CASE WHEN r.is_flagged = FALSE
                      THEN r.rating END), 2)         AS avg_rating,
       (SELECT COUNT(*) FROM problems p
        WHERE p.assigned_worker_id = wp.user_id
          AND p.status = 'completed')                AS completed_jobs,
       (SELECT ROUND(AVG(o.price), 2) FROM offers o
        WHERE o.worker_id = wp.user_id
          AND o.status = 'accepted')                 AS avg_job_price,
       (SELECT ROUND(AVG(TIMESTAMPDIFF(HOUR,
                p2.created_at, o2.created_at)), 1)
        FROM offers o2
        JOIN problems p2 ON p2.problem_id = o2.problem_id
        WHERE o2.worker_id = wp.user_id)             AS avg_response_hours
FROM worker_profiles wp
JOIN users u ON u.user_id = wp.user_id
LEFT JOIN reviews r ON r.worker_id = wp.user_id
GROUP BY wp.user_id, full_name, wp.headline, wp.service_area,
         wp.years_experience, wp.is_available;

-- Problem statistics: views, offers, offer conversion
CREATE VIEW v_problem_statistics AS
SELECT p.problem_id,
       p.title,
       c.name AS category,
       p.status,
       COUNT(DISTINCT pv.view_id)  AS total_views,
       COUNT(DISTINCT o.offer_id)  AS total_offers,
       ROUND(COUNT(DISTINCT o.offer_id) /
             NULLIF(COUNT(DISTINCT pv.view_id), 0) * 100, 1)
                                   AS offer_rate_pct
FROM problems p
JOIN categories c ON c.category_id = p.category_id
LEFT JOIN problem_views pv ON pv.problem_id = p.problem_id
LEFT JOIN offers o         ON o.problem_id  = p.problem_id
GROUP BY p.problem_id, p.title, c.name, p.status;

-- Category demand vs supply: open problems vs available workers
CREATE VIEW v_category_demand AS
SELECT c.category_id,
       c.name,
       COUNT(DISTINCT CASE WHEN p.status = 'open'
                           THEN p.problem_id END)  AS open_problems,
       COUNT(DISTINCT p.problem_id)                AS total_problems,
       COUNT(DISTINCT wc.user_id)                  AS workers_offering
FROM categories c
LEFT JOIN problems p           ON p.category_id  = c.category_id
LEFT JOIN worker_categories wc ON wc.category_id = c.category_id
GROUP BY c.category_id, c.name
ORDER BY open_problems DESC;

-- Most searched keywords
CREATE VIEW v_top_searches AS
SELECT keyword,
       COUNT(*) AS search_count
FROM search_logs
WHERE keyword IS NOT NULL AND keyword <> ''
GROUP BY keyword
ORDER BY search_count DESC;

-- Worker success rate: offers made vs accepted
CREATE VIEW v_worker_success AS
SELECT wp.user_id AS worker_id,
       CONCAT(u.first_name, ' ', u.last_name)        AS full_name,
       COUNT(o.offer_id)                             AS total_offers,
       SUM(o.status = 'accepted')                    AS accepted_offers,
       ROUND(SUM(o.status = 'accepted') /
             NULLIF(COUNT(o.offer_id), 0) * 100, 1)  AS acceptance_rate_pct
FROM worker_profiles wp
JOIN users u ON u.user_id = wp.user_id
LEFT JOIN offers o ON o.worker_id = wp.user_id
GROUP BY wp.user_id, full_name;

-- Registration growth per month (users vs new worker profiles)
CREATE VIEW v_registration_growth AS
SELECT m.month,
       m.new_users,
       COALESCE(w.new_workers, 0) AS new_workers
FROM (
    SELECT DATE_FORMAT(created_at, '%Y-%m') AS month,
           COUNT(*) AS new_users
    FROM users
    GROUP BY month
) m
LEFT JOIN (
    SELECT DATE_FORMAT(created_at, '%Y-%m') AS month,
           COUNT(*) AS new_workers
    FROM worker_profiles
    GROUP BY month
) w ON w.month = m.month
ORDER BY m.month;

-- ============================================================
-- 7. QUICK TESTS (run after loading mock data)
-- ============================================================
-- CALL sp_make_offer(5, 1, 120.00, 'I can fix this tomorrow', 'worker');
-- CALL sp_accept_offer(1);
-- CALL sp_complete_problem(1);
-- CALL sp_leave_review(1, 2, 5, 'Fast and clean work!');
-- SELECT fn_match_score(5, 1);
-- CALL sp_generate_recommendations(5);
-- SELECT * FROM recommendations WHERE worker_id = 5;
-- CALL sp_detect_fake_reviews();
-- SELECT * FROM v_worker_search ORDER BY avg_rating DESC;
-- SELECT * FROM v_category_demand;
-- SELECT * FROM v_problem_statistics ORDER BY total_offers DESC LIMIT 10;
