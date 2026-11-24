USE nextjob;

START TRANSACTION;

-- Offer notifications

UPDATE notifications
SET message_translations = JSON_OBJECT(
    'de', CONCAT(
        'Neues Angebot ',
        SUBSTRING_INDEX(SUBSTRING_INDEX(message, ')', 1), '(', -1),
        ' für deinen Auftrag #',
        SUBSTRING_INDEX(message, '#', -1)
    ),
    'sq', CONCAT(
        'Ofertë e re ',
        SUBSTRING_INDEX(SUBSTRING_INDEX(message, ')', 1), '(', -1),
        ' për kërkesën tënde #',
        SUBSTRING_INDEX(message, '#', -1)
    ),
    'en', message
)
WHERE type = 'offer'
AND message REGEXP '^New offer [(][0-9]+([.][0-9]+)?( ALL)?[)] on your problem #[0-9]+$'
AND message_translations IS NULL;


-- Review notifications

UPDATE notifications
SET message_translations = JSON_OBJECT(
    'de', CONCAT(
        'Du hast eine Bewertung mit ',
        SUBSTRING_INDEX(SUBSTRING_INDEX(message, '-star', 1), ' ', -1),
        ' Stern(en) erhalten.'
    ),
    'sq', CONCAT(
        'Ke marrë një vlerësim me ',
        SUBSTRING_INDEX(SUBSTRING_INDEX(message, '-star', 1), ' ', -1),
        ' yje.'
    ),
    'en', message
)
WHERE type = 'review'
AND message REGEXP '^You received a [1-5]-star review$'
AND message_translations IS NULL;


-- Chat notifications

UPDATE notifications
SET message_translations = JSON_OBJECT(
    'de', CONCAT(
        'Neue Nachricht von ',
        SUBSTRING(message, CHAR_LENGTH('New message from ') + 1)
    ),
    'sq', CONCAT(
        'Mesazh i ri nga ',
        SUBSTRING(message, CHAR_LENGTH('New message from ') + 1)
    ),
    'en', message
)
WHERE type = 'message'
AND message LIKE 'New message from %'
AND message_translations IS NULL;

COMMIT;