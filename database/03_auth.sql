-- ============================================================
-- NextJob - email verification + password reset
-- Loaded by deploy/reset_db.sh after 01 and 02.
-- ============================================================

ALTER TABLE users
    ADD COLUMN is_verified   BOOLEAN NOT NULL DEFAULT FALSE,
    ADD COLUMN token_version INT     NOT NULL DEFAULT 0;

CREATE TABLE auth_tokens (
    token_id   INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    user_id    INT UNSIGNED NOT NULL,      -- same type as users.user_id
    token_hash CHAR(64)     NOT NULL,      -- SHA-256 of the token, never the token
    purpose    ENUM('verify_email','reset_password') NOT NULL,
    expires_at DATETIME     NOT NULL,      -- stored in UTC
    used_at    DATETIME     NULL,
    created_at DATETIME     NOT NULL DEFAULT (UTC_TIMESTAMP()),
    CONSTRAINT fk_auth_tokens_user
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    UNIQUE KEY uq_token_hash (token_hash),
    INDEX idx_user_purpose (user_id, purpose)
) ENGINE=InnoDB;

-- The API user needs no extra grants: its rights on nextjob.* cover this table.
