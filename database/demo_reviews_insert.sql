-- ============================================================
-- NextJob — demo reviews for the Data-Science module
-- 30 reviews: 10 positive, 10 negative, 10 mixed
--
-- ADJUST BEFORE RUNNING:
--   * worker_id / customer_id / problem_id below must reference
--     EXISTING rows in your seed data (FK constraints!).
--   * If your reviews table has different column names, fix the
--     column list in line 1 of the INSERT.
-- Reviews are spread over workers 1-5, customers 6-15,
-- problems 1-30 (1:1). Texts are unique -> fake-review trigger
-- will not flag them.
-- ============================================================
USE nextjob;

INSERT INTO reviews (problem_id, worker_id, customer_id, rating, review_text) VALUES
(1, 1, 6, 5, 'He arrived exactly on time and fixed the leaking pipe perfectly. Great quality work for a very fair price.'),
(2, 2, 7, 5, 'Super friendly guy, explained everything patiently and the price was honest. Would hire again.'),
(3, 3, 8, 5, 'Replied to my request within minutes and came the same day. Very fast and professional.'),
(4, 4, 9, 5, 'Excellent quality, the new wiring works flawlessly. Also very punctual on both days.'),
(5, 5, 10, 5, 'Good price and solid work, my bathroom looks amazing now.'),
(6, 1, 11, 5, 'Very responsive, always answered my messages quickly. Kind and polite person.'),
(7, 2, 12, 5, 'Showed up right when he said he would and left everything clean and tidy. Real craftsmanship.'),
(8, 3, 13, 5, 'Fair quote and stuck to it, no hidden costs. The repair was done perfectly.'),
(9, 4, 14, 5, 'On time, friendly and the quality is top. Best worker I found on this platform.'),
(10, 5, 15, 5, 'Quick response, good price, quality job. Nothing to complain about.'),
(11, 1, 6, 1, 'Way too expensive for what he did. The final bill was double the estimate.'),
(12, 2, 7, 1, 'Showed up two hours late and was very rude when I asked why.'),
(13, 3, 8, 1, 'Terrible quality, the faucet broke again after a week and he ignores my calls now.'),
(14, 4, 9, 1, 'Extremely slow communication, took days to answer and then postponed twice.'),
(15, 5, 10, 2, 'Arrogant and impatient, talked down to me the whole time. Never again.'),
(16, 1, 11, 1, 'Sloppy job, he damaged my wall while working and refused to fix it.'),
(17, 2, 12, 1, 'Overpriced and unfriendly. Demanded extra money for no reason at the end.'),
(18, 3, 13, 1, 'Never arrived at the agreed time, kept me waiting all morning without a word.'),
(19, 4, 14, 1, 'Bad work quality, crooked tiles and the leak came back two days later.'),
(20, 5, 15, 2, 'Impossible to reach after the first visit, stopped responding completely.'),
(21, 1, 6, 3, 'The work quality is really good, but he came very late both days.'),
(22, 2, 7, 3, 'Friendly and polite, however way too expensive for such a simple job.'),
(23, 3, 8, 3, 'Fixed everything perfectly, sadly the communication was painfully slow.'),
(24, 4, 9, 3, 'Arrived on time and worked fast, but the price was much higher than quoted.'),
(25, 5, 10, 3, 'Great quality result, unfortunately he was quite rude when I asked questions.'),
(26, 1, 11, 2, 'Cheap and quick response, but the paint job is already peeling. Poor quality.'),
(27, 2, 12, 4, 'Punctual and fair price. The quality is okay, but he left a small mess.'),
(28, 3, 13, 4, 'Very fast reply and came the next morning. Price was fair, quality decent.'),
(29, 4, 14, 4, 'Nice person and honest pricing, though he arrived a bit late.'),
(30, 5, 15, 4, 'Solid quality and very friendly, response time could be faster.');