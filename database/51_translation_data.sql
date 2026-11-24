USE nextjob;

UPDATE categories
SET name_translations = JSON_OBJECT(
    'de',
    CASE name
        WHEN 'Plumber' THEN 'Installateur'
        WHEN 'Electrician' THEN 'Elektriker'
        WHEN 'Painter' THEN 'Maler'
        WHEN 'Carpenter' THEN 'Tischler'
        WHEN 'Mason' THEN 'Maurer'
        WHEN 'Roofer' THEN 'Dachdecker'
        WHEN 'HVAC Technician' THEN 'Klimatechniker'
        WHEN 'Gardener' THEN 'Gärtner'
        WHEN 'Cleaner' THEN 'Reinigungskraft'
        WHEN 'Locksmith' THEN 'Schlosser'
        WHEN 'Tiler' THEN 'Fliesenleger'
        WHEN 'Welder' THEN 'Schweißer'
        WHEN 'Appliance Repair' THEN 'Gerätereparatur'
        WHEN 'Moving & Transport' THEN 'Umzug und Transport'
        WHEN 'General Handyman' THEN 'Allround-Handwerker'
        ELSE name
    END,
    'sq',
    CASE name
        WHEN 'Plumber' THEN 'Hidraulik'
        WHEN 'Electrician' THEN 'Elektricist'
        WHEN 'Painter' THEN 'Bojaxhi'
        WHEN 'Carpenter' THEN 'Marangoz'
        WHEN 'Mason' THEN 'Murator'
        WHEN 'Roofer' THEN 'Mjeshtër çatie'
        WHEN 'HVAC Technician' THEN 'Teknik klimatizimi'
        WHEN 'Gardener' THEN 'Kopshtar'
        WHEN 'Cleaner' THEN 'Pastrues'
        WHEN 'Locksmith' THEN 'Çelësabërës'
        WHEN 'Tiler' THEN 'Pllakashtrues'
        WHEN 'Welder' THEN 'Saldator'
        WHEN 'Appliance Repair' THEN 'Riparim pajisjesh'
        WHEN 'Moving & Transport' THEN 'Zhvendosje dhe transport'
        WHEN 'General Handyman' THEN 'Mjeshtër i përgjithshëm'
        ELSE name
    END,
    'en', name
);