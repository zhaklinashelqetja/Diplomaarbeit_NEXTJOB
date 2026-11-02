-- ============================================================
-- NextJob - email verification + password reset tokens
-- Loaded by deploy/reset_db.sh after 01 and 02.
-- (users.is_verified and users.token_version are now in 01.)
-- ============================================================

CREATE TABLE auth_tokens (
    token_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id    INT          NOT NULL,
    token_hash CHAR(64)     NOT NULL,      -- SHA-256 of the token, never the token
    purpose    ENUM('verify_email','reset_password') NOT NULL,
    expires_at DATETIME     NOT NULL,      -- stored in UTC
    used_at    DATETIME     NULL,
    created_at DATETIME     NOT NULL DEFAULT (UTC_TIMESTAMP()),
    CONSTRAINT fk_auth_tokens_user
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    CONSTRAINT uq_token_hash UNIQUE (token_hash)
);

-- The API user needs no extra grants: its rights on nextjob.* cover this table.
