-- ============================================================
-- NextJob - what the user chose at registration
-- Loaded by deploy/reset_db.sh after 03.
--
-- jobgeber  = looks for services
-- jobnehmer = offers services
-- NULL      = existing users / no choice made
-- A user can still do both; becoming a worker stays POST /api/workers/me.
-- ============================================================

ALTER TABLE users
    ADD COLUMN account_type ENUM('jobgeber','jobnehmer') NULL DEFAULT NULL
        AFTER location;
