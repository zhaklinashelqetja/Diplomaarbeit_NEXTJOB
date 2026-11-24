USE nextjob;

DROP TRIGGER IF EXISTS trg_offer_notify;
DROP TRIGGER IF EXISTS trg_offer_status;
DROP TRIGGER IF EXISTS trg_problem_status;
DROP TRIGGER IF EXISTS trg_review_notify;

DELIMITER //

CREATE TRIGGER trg_offer_notify
AFTER INSERT ON offers
FOR EACH ROW
BEGIN
    INSERT INTO notifications
        (user_id, type, message, message_translations)
    SELECT p.customer_id, 'offer',
        CONCAT('New offer (', NEW.price,
               ' ALL) on your problem #', NEW.problem_id),
        JSON_OBJECT(
            'de', CONCAT('Neues Angebot (', NEW.price,
                         ' ALL) für deinen Auftrag #', NEW.problem_id),
            'sq', CONCAT('Ofertë e re (', NEW.price,
                         ' ALL) për kërkesën tënde #', NEW.problem_id),
            'en', CONCAT('New offer (', NEW.price,
                         ' ALL) on your problem #', NEW.problem_id)
        )
    FROM problems p
    WHERE p.problem_id = NEW.problem_id;
END //


CREATE TRIGGER trg_offer_status
AFTER UPDATE ON offers
FOR EACH ROW
BEGIN
    IF NEW.status <> OLD.status THEN
        INSERT INTO notifications
            (user_id, type, message, message_translations)
        VALUES (
            NEW.worker_id,
            'offer',
            CONCAT('Your offer on problem #', NEW.problem_id,
                   ' is now: ', NEW.status),
            JSON_OBJECT(
                'de', CONCAT(
                    'Dein Angebot für Auftrag #', NEW.problem_id,
                    ': ',
                    CASE NEW.status
                        WHEN 'pending' THEN 'Ausstehend'
                        WHEN 'accepted' THEN 'Angenommen'
                        WHEN 'rejected' THEN 'Abgelehnt'
                        WHEN 'withdrawn' THEN 'Zurückgezogen'
                        ELSE NEW.status
                    END
                ),
                'sq', CONCAT(
                    'Oferta jote për kërkesën #', NEW.problem_id,
                    ': ',
                    CASE NEW.status
                        WHEN 'pending' THEN 'Në pritje'
                        WHEN 'accepted' THEN 'Pranuar'
                        WHEN 'rejected' THEN 'Refuzuar'
                        WHEN 'withdrawn' THEN 'Tërhequr'
                        ELSE NEW.status
                    END
                ),
                'en', CONCAT(
                    'Your offer on problem #', NEW.problem_id,
                    ' is now: ', NEW.status
                )
            )
        );
    END IF;
END //


CREATE TRIGGER trg_problem_status
AFTER UPDATE ON problems
FOR EACH ROW
BEGIN
    IF NEW.status <> OLD.status THEN

        IF NEW.assigned_worker_id IS NOT NULL THEN
            INSERT INTO notifications
                (user_id, type, message, message_translations)
            VALUES (
                NEW.assigned_worker_id,
                'job',
                CONCAT('Job #', NEW.problem_id,
                       ' is now: ', NEW.status),
                JSON_OBJECT(
                    'de', CONCAT(
                        'Auftrag #', NEW.problem_id, ': ',
                        CASE NEW.status
                            WHEN 'open' THEN 'Offen'
                            WHEN 'assigned' THEN 'Zugewiesen'
                            WHEN 'in_progress' THEN 'In Bearbeitung'
                            WHEN 'completed' THEN 'Abgeschlossen'
                            WHEN 'cancelled' THEN 'Storniert'
                            ELSE NEW.status
                        END
                    ),
                    'sq', CONCAT(
                        'Puna #', NEW.problem_id, ': ',
                        CASE NEW.status
                            WHEN 'open' THEN 'E hapur'
                            WHEN 'assigned' THEN 'E caktuar'
                            WHEN 'in_progress' THEN 'Në proces'
                            WHEN 'completed' THEN 'E përfunduar'
                            WHEN 'cancelled' THEN 'E anuluar'
                            ELSE NEW.status
                        END
                    ),
                    'en', CONCAT(
                        'Job #', NEW.problem_id,
                        ' is now: ', NEW.status
                    )
                )
            );
        END IF;

        IF NEW.status = 'completed' THEN
            INSERT INTO notifications
                (user_id, type, message, message_translations)
            VALUES (
                NEW.customer_id,
                'review',
                CONCAT('Job #', NEW.problem_id,
                       ' completed — leave a review for the worker!'),
                JSON_OBJECT(
                    'de', CONCAT(
                        'Auftrag #', NEW.problem_id,
                        ' abgeschlossen – bewerte den Handwerker!'
                    ),
                    'sq', CONCAT(
                        'Puna #', NEW.problem_id,
                        ' përfundoi – vlerëso mjeshtrin!'
                    ),
                    'en', CONCAT(
                        'Job #', NEW.problem_id,
                        ' completed — leave a review for the worker!'
                    )
                )
            );
        END IF;

    END IF;
END //


CREATE TRIGGER trg_review_notify
AFTER INSERT ON reviews
FOR EACH ROW
BEGIN
    INSERT INTO notifications
        (user_id, type, message, message_translations)
    VALUES (
        NEW.worker_id,
        'review',
        CONCAT('You received a ', NEW.rating, '-star review'),
        JSON_OBJECT(
            'de', CONCAT('Du hast eine Bewertung mit ',
                         NEW.rating, ' Stern(en) erhalten.'),
            'sq', CONCAT('Ke marrë një vlerësim me ',
                         NEW.rating, ' yje.'),
            'en', CONCAT('You received a ',
                         NEW.rating, '-star review')
        )
    );
END //

DELIMITER ;