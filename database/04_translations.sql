USE nextjob;

ALTER TABLE categories
    ADD COLUMN name_translations JSON NULL;

ALTER TABLE problems
    ADD COLUMN title_translations JSON NULL,
    ADD COLUMN description_translations JSON NULL;

ALTER TABLE worker_profiles
    ADD COLUMN headline_translations JSON NULL,
    ADD COLUMN bio_translations JSON NULL;

ALTER TABLE reviews
    ADD COLUMN review_text_translations JSON NULL,
    ADD COLUMN flag_reason_translations JSON NULL;

ALTER TABLE offers
    ADD COLUMN message_translations JSON NULL;

ALTER TABLE notifications
    ADD COLUMN message_translations JSON NULL;

ALTER TABLE messages
    ADD COLUMN content_translations JSON NULL;

ALTER TABLE ai_conversations
    ADD COLUMN title_translations JSON NULL;

ALTER TABLE ai_messages
    ADD COLUMN content_translations JSON NULL;
