-- ============================================================
-- NextJob — Test Seed Data
-- Run AFTER nextjob.sql on a FRESH database (explicit IDs!).
-- Requires: users.password_hash = VARCHAR(255)
--
-- Every user's password is:  test1234
-- (same werkzeug hash for all -> you can log in via the API
--  with any email below, e.g. arben.hoxha@test.al / test1234)
-- ============================================================
USE nextjob;

SET @pw = 'scrypt:32768:8:1$Nrg69F0hLHJPAzpp$3e8583384c40aa1a1543193652734076502b69e20b59108506f233492b78e3e9ca7a99749484047c8c1d367e872436ae5951be7a5637c43a51c86fbf6b3938d5';

-- ---------- users (1 admin, 20 members) ----------
INSERT INTO users (user_id, is_admin, first_name, last_name, email, password_hash, phone, location) VALUES
( 1, TRUE , 'Admin' , 'NextJob'  , 'admin@nextjob.al'        , @pw, '0690000000', 'Shkoder'),
( 2, FALSE, 'Arben' , 'Hoxha'    , 'arben.hoxha@test.al'     , @pw, '0691111111', 'Shkoder'),
( 3, FALSE, 'Elira' , 'Marku'    , 'elira.marku@test.al'     , @pw, '0692222222', 'Shkoder'),
( 4, FALSE, 'Drin'  , 'Leka'     , 'drin.leka@test.al'       , @pw, '0693333333', 'Tirana'),
( 5, FALSE, 'Sara'  , 'Doda'     , 'sara.doda@test.al'       , @pw, '0694444444', 'Durres'),
( 6, FALSE, 'Besnik', 'Gjoka'    , 'besnik.gjoka@test.al'    , @pw, '0695555555', 'Shkoder'),
( 7, FALSE, 'Luan'  , 'Prendi'   , 'luan.prendi@test.al'     , @pw, '0696666666', 'Shkoder'),
( 8, FALSE, 'Mira'  , 'Shkreli'  , 'mira.shkreli@test.al'    , @pw, '0697777777', 'Tirana'),
( 9, FALSE, 'Gent'  , 'Kola'     , 'gent.kola@test.al'       , @pw, '0698888888', 'Shkoder'),
(10, FALSE, 'Ermal' , 'Bushati'  , 'ermal.bushati@test.al'   , @pw, '0699999999', 'Lezha'),
(11, FALSE, 'Klara' , 'Nika'     , 'klara.nika@test.al'      , @pw, '0681111111', 'Shkoder'),
(12, FALSE, 'Endri' , 'Vata'     , 'endri.vata@test.al'      , @pw, '0682222222', 'Tirana'),
(13, FALSE, 'Anda'  , 'Curri'    , 'anda.curri@test.al'      , @pw, '0683333333', 'Durres'),
(14, FALSE, 'Redon' , 'Basha'    , 'redon.basha@test.al'     , @pw, '0684444444', 'Shkoder'),
(15, FALSE, 'Jonida', 'Frashëri' , 'jonida.frasheri@test.al' , @pw, '0685555555', 'Tirana'),
(16, FALSE, 'Altin' , 'Deda'     , 'altin.deda@test.al'      , @pw, '0686666666', 'Shkoder'),
(17, FALSE, 'Vera'  , 'Lleshi'   , 'vera.lleshi@test.al'     , @pw, '0687777777', 'Lezha'),
(18, FALSE, 'Kreshnik','Mali'    , 'kreshnik.mali@test.al'   , @pw, '0688888888', 'Shkoder'),
(19, FALSE, 'Dea'   , 'Rrota'    , 'dea.rrota@test.al'       , @pw, '0689999999', 'Tirana'),
(20, FALSE, 'Olti'  , 'Zefi'     , 'olti.zefi@test.al'       , @pw, '0671111111', 'Shkoder'),
(21, FALSE, 'Rina'  , 'Kastrati' , 'rina.kastrati@test.al'   , @pw, '0672222222', 'Durres');

-- ---------- worker profiles (users 6-13 are workers; 13 is ALSO a customer below) ----------
INSERT INTO worker_profiles (user_id, headline, bio, years_experience, service_area, is_available) VALUES
( 6, 'Master plumber — fast & clean', 'Plumbing since 2014, emergency jobs welcome.', 12, 'Shkoder', TRUE),
( 7, 'Certified electrician',        'Installations, repairs, smart home wiring.',    8, 'Shkoder', TRUE),
( 8, 'Painter & decorator',          'Interior and exterior painting.',               5, 'Tirana' , TRUE),
( 9, 'Carpenter — custom furniture', 'Doors, windows, kitchens, repairs.',           15, 'Shkoder', TRUE),
(10, 'General handyman',             'Small fixes of every kind.',                    4, 'Lezha'  , TRUE),
(11, 'Cleaner — homes & offices',    'Deep cleaning, move-out cleaning.',             3, 'Shkoder', TRUE),
(12, 'Electrician & appliance repair','Washing machines, ovens, wiring.',             7, 'Tirana' , FALSE),
(13, 'Tiler & mason',                'Bathrooms, kitchens, terraces.',               10, 'Durres' , TRUE);

-- ---------- worker trades ----------
INSERT INTO worker_categories (user_id, category_id) VALUES
(6,1),                 -- Besnik: plumber
(7,2),(7,13),          -- Luan: electrician + appliance repair
(8,3),                 -- Mira: painter
(9,4),(9,15),          -- Gent: carpenter + general handyman
(10,15),(10,1),        -- Ermal: handyman + plumber
(11,9),                -- Klara: cleaner
(12,2),(12,13),        -- Endri: electrician + appliance repair
(13,11),(13,5);        -- Anda: tiler + mason

-- ---------- problems ----------
-- status mix: 6 open, 2 assigned, 1 in_progress, 4 completed, 1 cancelled
INSERT INTO problems (problem_id, customer_id, category_id, title, description, location, contact_phone, budget, urgency, preferred_date, status, assigned_worker_id) VALUES
( 1, 2, 1, 'Leaking pipe under kitchen sink', 'Water dripping constantly, cabinet is getting damaged.', 'Shkoder', '0691111111', 60.00 , 'high'     , NULL        , 'open'       , NULL),
( 2, 3, 2, 'Power socket sparks',             'Living room socket sparks when plugging in the heater.', 'Shkoder', '0692222222', 40.00 , 'emergency', NULL        , 'open'       , NULL),
( 3, 4, 3, 'Repaint two bedrooms',            'Two rooms approx. 15m2 each, white, walls in good shape.','Tirana' , '0693333333', 250.00, 'normal'   , '2026-07-20', 'open'       , NULL),
( 4, 5, 11,'Bathroom tiles cracked',          'About 2m2 of floor tiles need replacement.',              'Durres' , '0694444444', 150.00, 'normal'   , NULL        , 'open'       , NULL),
( 5, 2, 15,'Mount TV and shelves',            'One 55 inch TV and three wall shelves.',                  'Shkoder', '0691111111', 50.00 , 'low'      , NULL        , 'open'       , NULL),
( 6,14, 9, 'Deep clean after renovation',     'Apartment 80m2, lots of dust, windows included.',         'Shkoder', '0684444444', 120.00, 'normal'   , '2026-07-15', 'open'       , NULL),
( 7,15, 2, 'Install ceiling lamps',           'Five lamps, cables already in place.',                    'Tirana' , '0685555555', 80.00 , 'normal'   , NULL        , 'assigned'   , 12),
( 8,16, 1, 'Boiler makes loud noise',         'Boiler bangs when heating starts.',                       'Shkoder', '0686666666', 100.00, 'high'     , NULL        , 'assigned'   , 6),
( 9,17, 4, 'Fix jammed front door',           'Door frame swollen, door barely closes.',                 'Lezha'  , '0687777777', 70.00 , 'high'     , NULL        , 'in_progress', 9),
(10,18, 1, 'Replace bathroom faucet',         'Old faucet leaks, new one already bought.',               'Shkoder', '0688888888', 35.00 , 'normal'   , NULL        , 'completed'  , 6),
(11,19, 13,'Washing machine not spinning',    'Machine fills and drains but drum does not spin.',        'Tirana' , '0689999999', 90.00 , 'high'     , NULL        , 'completed'  , 12),
(12,20, 3, 'Paint balcony railing',           'Metal railing, approx 6m, rust removal included.',        'Shkoder', '0671111111', 60.00 , 'low'      , NULL        , 'completed'  , 8),
(13,21, 15,'Assemble IKEA wardrobe',          'PAX wardrobe 2m, instructions available.',                'Durres' , '0672222222', 45.00 , 'normal'   , NULL        , 'completed'  , 10),
(14, 3, 9, 'Weekly cleaning offer wanted',    'Looking for recurring cleaning, cancelled for now.',      'Shkoder', '0692222222', NULL  , 'low'      , NULL        , 'cancelled'  , NULL),
(15,13, 1, 'Water heater installation',       'New 80l heater to install in bathroom (worker posting as customer).','Durres','0683333333', 130.00,'normal', NULL   , 'open'       , NULL);

-- ---------- problem photos ----------
INSERT INTO problem_photos (problem_id, file_path, sort_order) VALUES
( 1,'/uploads/problems/p1_sink_1.jpg',0),( 1,'/uploads/problems/p1_sink_2.jpg',1),
( 2,'/uploads/problems/p2_socket.jpg',0),
( 3,'/uploads/problems/p3_room_a.jpg',0),( 3,'/uploads/problems/p3_room_b.jpg',1),
( 4,'/uploads/problems/p4_tiles.jpg',0),
( 6,'/uploads/problems/p6_dust_1.jpg',0),( 6,'/uploads/problems/p6_dust_2.jpg',1),( 6,'/uploads/problems/p6_dust_3.jpg',2),
( 8,'/uploads/problems/p8_boiler.jpg',0),
( 9,'/uploads/problems/p9_door.jpg',0),
(10,'/uploads/problems/p10_faucet.jpg',0),
(11,'/uploads/problems/p11_machine.jpg',0);

-- ---------- offers ----------
-- pending offers on open problems + accepted/rejected history on finished ones
-- (INSERT triggers create employer notifications automatically)
INSERT INTO offers (offer_id, problem_id, worker_id, price, message, initiated_by, status) VALUES
-- open problems: competing pending offers
( 1, 1, 6, 55.00 , 'Can come today after 17:00.'          ,'worker'  ,'pending'),
( 2, 1,10, 45.00 , 'Tomorrow morning, 1h job.'            ,'worker'  ,'pending'),
( 3, 2, 7, 35.00 , 'Sounds like a loose contact, quick fix.','worker' ,'pending'),
( 4, 2,12, 40.00 , 'Available Saturday.'                  ,'customer','pending'),
( 5, 3, 8, 230.00, 'Including paint and materials.'       ,'worker'  ,'pending'),
( 6, 4,13, 140.00, 'Have matching tiles in stock.'        ,'worker'  ,'pending'),
( 7, 5, 9, 40.00 , 'Can do it this week.'                 ,'worker'  ,'pending'),
( 8, 5,10, 35.00 , 'Tomorrow possible.'                   ,'worker'  ,'pending'),
( 9, 6,11, 110.00, 'Two of us, done in one day.'          ,'worker'  ,'pending'),
-- assigned / in_progress: one accepted, rivals rejected
(10, 7,12, 75.00 , 'All five in one visit.'               ,'worker'  ,'accepted'),
(11, 7, 7, 85.00 , 'Can start Monday.'                    ,'worker'  ,'rejected'),
(12, 8, 6, 95.00 , 'Probably the expansion vessel.'       ,'customer','accepted'),
(13, 9, 9, 65.00 , 'Will plane the door on site.'         ,'worker'  ,'accepted'),
-- completed: accepted offer that matches assigned_worker_id
(14,10, 6, 30.00 , 'Quick swap, 30 minutes.'              ,'worker'  ,'accepted'),
(15,10,10, 38.00 , 'Can come tonight.'                    ,'worker'  ,'rejected'),
(16,11,12, 85.00 , 'Likely the drive belt.'               ,'worker'  ,'accepted'),
(17,12, 8, 55.00 , 'Rust treatment plus two coats.'       ,'worker'  ,'accepted'),
(18,13,10, 40.00 , 'Assembled many of these.'             ,'worker'  ,'accepted'),
-- one withdrawn example
(19, 3, 9, 260.00, 'Changed my mind, too far away.'       ,'worker'  ,'withdrawn');

-- ---------- reviews (only for completed problems, 1 per problem) ----------
-- NOTE: reviews 3 and 4 have IDENTICAL text on purpose ->
-- the trg_review_duplicate trigger flags the second one instantly (demo!)
INSERT INTO reviews (review_id, problem_id, worker_id, customer_id, rating, review_text) VALUES
(1, 10, 6, 18, 5, 'Besnik was fast and very tidy, faucet works perfectly.'),
(2, 11, 12, 19, 4, 'Machine fixed, took a bit longer than promised but fair price.'),
(3, 12, 8, 20, 5, 'Great work, highly recommended!'),
(4, 13, 10, 21, 5, 'Great work, highly recommended!');

-- ---------- messages ----------
INSERT INTO messages (sender_id, receiver_id, problem_id, content, is_read) VALUES
( 2, 6, 1, 'Hi, is the price fixed or can you check first?', TRUE),
( 6, 2, 1, 'I will check first, price is the maximum.', TRUE),
( 3, 7, 2, 'How fast can you come? It smells burnt.', TRUE),
( 7, 3, 2, 'Turn off that fuse! I can be there in an hour.', FALSE),
(15,12, 7, 'Monday 10:00 works for me.', TRUE),
(12,15, 7, 'Perfect, see you then.', FALSE),
(16, 6, 8, 'Boiler is in the basement, I will be home all day.', TRUE),
( 5,13, 4, 'Do you have the tiles in light gray?', FALSE);

-- ---------- problem views (for statistics) ----------
INSERT INTO problem_views (problem_id, user_id) VALUES
(1,6),(1,10),(1,NULL),(1,NULL),(2,7),(2,12),(2,NULL),(3,8),(3,9),(3,NULL),
(4,13),(5,9),(5,10),(5,NULL),(6,11),(6,NULL),(7,12),(7,7),(8,6),(9,9),
(10,6),(10,10),(10,NULL),(11,12),(12,8),(13,10),(15,6),(15,10),(1,7),(2,NULL);

-- ---------- search logs (for v_top_searches) ----------
INSERT INTO search_logs (user_id, keyword, category_filter, location_filter) VALUES
( 2,'plumber'      ,1   ,'Shkoder'),( 3,'electrician',2 ,'Shkoder'),
( 4,'painter'      ,3   ,'Tirana') ,( 5,'tiles'      ,11,'Durres'),
(14,'cleaning'     ,9   ,'Shkoder'),(16,'plumber'    ,1 ,'Shkoder'),
(18,'plumber'      ,1   ,NULL)     ,(19,'washing machine',13,'Tirana'),
(NULL,'electrician',2   ,NULL)     ,(NULL,'plumber'  ,NULL,'Shkoder'),
(20,'painter'      ,3   ,'Shkoder'),(21,'furniture assembly',15,NULL);

-- ---------- saved bookmarks ----------
INSERT INTO saved_workers (customer_id, worker_id) VALUES
(2,6),(2,10),(3,7),(16,6),(18,6),(19,12);
INSERT INTO saved_problems (worker_id, problem_id) VALUES
(6,15),(10,1),(10,5),(8,3),(13,4),(11,6);

-- ---------- AI assistant demo data ----------
INSERT INTO ai_conversations (conversation_id, user_id, title) VALUES
(1, 2, 'How do I choose a plumber?'),
(2, 6, 'How can I get more jobs?');
INSERT INTO ai_messages (conversation_id, sender, content) VALUES
(1,'user'     ,'I have two offers for my leaking pipe, how do I pick?'),
(1,'assistant','Compare the workers'' ratings, completed jobs and response time — both are visible on their profiles.'),
(2,'user'     ,'My offers keep getting rejected, any tips?'),
(2,'assistant','Workers with a complete profile, photos and fast responses get accepted more often.');

-- ---------- refresh For You feeds for all workers ----------
CALL sp_generate_recommendations(6);
CALL sp_generate_recommendations(7);
CALL sp_generate_recommendations(8);
CALL sp_generate_recommendations(9);
CALL sp_generate_recommendations(10);
CALL sp_generate_recommendations(11);
CALL sp_generate_recommendations(12);
CALL sp_generate_recommendations(13);

-- ============================================================
-- Quick verification queries
-- ============================================================
-- SELECT * FROM v_worker_search ORDER BY avg_rating DESC;
-- SELECT * FROM v_category_demand;
-- SELECT * FROM v_problem_statistics ORDER BY total_offers DESC;
-- SELECT * FROM v_top_searches;
-- SELECT * FROM reviews WHERE is_flagged = TRUE;   -- duplicate demo
-- SELECT * FROM recommendations ORDER BY worker_id, score DESC;
