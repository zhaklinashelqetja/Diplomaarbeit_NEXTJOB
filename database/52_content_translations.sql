USE nextjob;

START TRANSACTION;

-- Problems

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Undichtes Rohr unter der Küchenspüle',
        'sq', 'Tub që rrjedh poshtë lavamanit të kuzhinës',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Wasser tropft ständig, der Unterschrank wird beschädigt.',
        'sq', 'Uji pikon vazhdimisht dhe dollapi po dëmtohet.',
        'en', description
    )
WHERE title = 'Leaking pipe under kitchen sink'
AND description = 'Water dripping constantly, cabinet is getting damaged.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Steckdose erzeugt Funken',
        'sq', 'Priza elektrike lëshon shkëndija',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Die Steckdose im Wohnzimmer erzeugt Funken, wenn das Heizgerät angeschlossen wird.',
        'sq', 'Priza në dhomën e ndenjjes lëshon shkëndija kur lidhet ngrohësja.',
        'en', description
    )
WHERE title = 'Power socket sparks'
AND description = 'Living room socket sparks when plugging in the heater.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Zwei Schlafzimmer neu streichen',
        'sq', 'Lyerja e dy dhomave të gjumit',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Zwei Zimmer mit jeweils ca. 15 m², weiß, Wände in gutem Zustand.',
        'sq', 'Dy dhoma me nga rreth 15 m², ngjyrë e bardhë, muret në gjendje të mirë.',
        'en', description
    )
WHERE title = 'Repaint two bedrooms'
AND description = 'Two rooms approx. 15m2 each, white, walls in good shape.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Beschädigte Badezimmerfliesen',
        'sq', 'Pllaka të çara në banjë',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Etwa 2 m² Bodenfliesen müssen ersetzt werden.',
        'sq', 'Duhet të zëvendësohen rreth 2 m² pllaka dyshemeje.',
        'en', description
    )
WHERE title = 'Bathroom tiles cracked'
AND description = 'About 2m2 of floor tiles need replacement.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Fernseher und Regale montieren',
        'sq', 'Montimi i televizorit dhe rafteve',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Ein 55-Zoll-Fernseher und drei Wandregale.',
        'sq', 'Një televizor 55 inç dhe tre rafte muri.',
        'en', description
    )
WHERE title = 'Mount TV and shelves'
AND description = 'One 55 inch TV and three wall shelves.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Grundreinigung nach Renovierung',
        'sq', 'Pastrim i thelluar pas rinovimit',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Wohnung mit 80 m², viel Staub, inklusive Fensterreinigung.',
        'sq', 'Apartament 80 m², shumë pluhur, përfshirë pastrimin e dritareve.',
        'en', description
    )
WHERE title = 'Deep clean after renovation'
AND description = 'Apartment 80m2, lots of dust, windows included.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Deckenlampen installieren',
        'sq', 'Montimi i llambave të tavanit',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Fünf Lampen, Kabel sind bereits vorhanden.',
        'sq', 'Pesë llamba, kabllot janë vendosur tashmë.',
        'en', description
    )
WHERE title = 'Install ceiling lamps'
AND description = 'Five lamps, cables already in place.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Heizkessel macht laute Geräusche',
        'sq', 'Kaldaja bën zhurmë të fortë',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Der Heizkessel macht klopfende Geräusche, wenn die Heizung startet.',
        'sq', 'Kaldaja bën zhurma goditëse kur fillon ngrohja.',
        'en', description
    )
WHERE title = 'Boiler makes loud noise'
AND description = 'Boiler bangs when heating starts.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Klemmende Eingangstür reparieren',
        'sq', 'Riparimi i derës së hyrjes që ngec',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Der Türrahmen ist aufgequollen, die Tür schließt kaum.',
        'sq', 'Korniza e derës është fryrë dhe dera mezi mbyllet.',
        'en', description
    )
WHERE title = 'Fix jammed front door'
AND description = 'Door frame swollen, door barely closes.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Wasserhahn im Badezimmer ersetzen',
        'sq', 'Zëvendësimi i rubinetit të banjës',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Der alte Wasserhahn ist undicht, ein neuer wurde bereits gekauft.',
        'sq', 'Rubineti i vjetër rrjedh, një i ri është blerë tashmë.',
        'en', description
    )
WHERE title = 'Replace bathroom faucet'
AND description = 'Old faucet leaks, new one already bought.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Waschmaschine schleudert nicht',
        'sq', 'Lavatriçja nuk centrifugon',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Die Maschine nimmt Wasser auf und pumpt es ab, aber die Trommel dreht sich nicht.',
        'sq', 'Lavatriçja mbushet me ujë dhe e shkarkon atë, por kazani nuk rrotullohet.',
        'en', description
    )
WHERE title = 'Washing machine not spinning'
AND description = 'Machine fills and drains but drum does not spin.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Balkongeländer streichen',
        'sq', 'Lyerja e parmakut të ballkonit',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Metallgeländer, ca. 6 m, inklusive Rostentfernung.',
        'sq', 'Parmak metalik, rreth 6 m, përfshirë heqjen e ndryshkut.',
        'en', description
    )
WHERE title = 'Paint balcony railing'
AND description = 'Metal railing, approx 6m, rust removal included.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'IKEA-Kleiderschrank aufbauen',
        'sq', 'Montimi i dollapit IKEA',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'PAX-Kleiderschrank, 2 m, Montageanleitung vorhanden.',
        'sq', 'Dollap PAX, 2 m, udhëzimet e montimit janë në dispozicion.',
        'en', description
    )
WHERE title = 'Assemble IKEA wardrobe'
AND description = 'PAX wardrobe 2m, instructions available.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Angebot für wöchentliche Reinigung gesucht',
        'sq', 'Kërkohet ofertë për pastrim javor',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Regelmäßige Reinigung gesucht, vorerst storniert.',
        'sq', 'Kërkohet pastrim i rregullt, për momentin i anuluar.',
        'en', description
    )
WHERE title = 'Weekly cleaning offer wanted'
AND description = 'Looking for recurring cleaning, cancelled for now.';

UPDATE problems SET
    title_translations = JSON_OBJECT(
        'de', 'Warmwasserboiler installieren',
        'sq', 'Instalimi i bojlerit të ujit',
        'en', title
    ),
    description_translations = JSON_OBJECT(
        'de', 'Neuer 80-Liter-Boiler zur Installation im Badezimmer (Handwerker erstellt Auftrag als Kunde).',
        'sq', 'Bojler i ri 80 litra për instalim në banjë (mjeshtri publikon kërkesën si klient).',
        'en', description
    )
WHERE title = 'Water heater installation'
AND description = 'New 80l heater to install in bathroom (worker posting as customer).';


-- Worker profiles

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Installateurmeister – schnell und sauber',
        'sq', 'Mjeshtër hidraulik – i shpejtë dhe i pastër',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Installateur seit 2014, auch für Notfälle verfügbar.',
        'sq', 'Hidraulik që nga viti 2014, i disponueshëm edhe për raste urgjente.',
        'en', bio
    )
WHERE headline = 'Master plumber — fast & clean'
AND bio = 'Plumbing since 2014, emergency jobs welcome.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Zertifizierter Elektriker',
        'sq', 'Elektricist i certifikuar',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Installationen, Reparaturen und Smart-Home-Verkabelung.',
        'sq', 'Instalime, riparime dhe kabllime për shtëpi inteligjente.',
        'en', bio
    )
WHERE headline = 'Certified electrician'
AND bio = 'Installations, repairs, smart home wiring.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Maler und Dekorateur',
        'sq', 'Bojaxhi dhe dekorues',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Malerarbeiten im Innen- und Außenbereich.',
        'sq', 'Lyerje të ambienteve të brendshme dhe të jashtme.',
        'en', bio
    )
WHERE headline = 'Painter & decorator'
AND bio = 'Interior and exterior painting.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Tischler – Möbel nach Maß',
        'sq', 'Marangoz – mobilie sipas porosisë',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Türen, Fenster, Küchen und Reparaturen.',
        'sq', 'Dyer, dritare, kuzhina dhe riparime.',
        'en', bio
    )
WHERE headline = 'Carpenter — custom furniture'
AND bio = 'Doors, windows, kitchens, repairs.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Allround-Handwerker',
        'sq', 'Mjeshtër i përgjithshëm',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Kleine Reparaturen aller Art.',
        'sq', 'Riparime të vogla të çdo lloji.',
        'en', bio
    )
WHERE headline = 'General handyman'
AND bio = 'Small fixes of every kind.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Reinigungskraft – Wohnungen und Büros',
        'sq', 'Pastrues – banesa dhe zyra',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Grundreinigung und Reinigung nach dem Auszug.',
        'sq', 'Pastrim i thelluar dhe pastrim pas largimit nga banesa.',
        'en', bio
    )
WHERE headline = 'Cleaner — homes & offices'
AND bio = 'Deep cleaning, move-out cleaning.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Elektriker und Gerätereparatur',
        'sq', 'Elektricist dhe riparues pajisjesh',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Waschmaschinen, Backöfen und elektrische Verkabelung.',
        'sq', 'Lavatriçe, furra dhe kabllime elektrike.',
        'en', bio
    )
WHERE headline = 'Electrician & appliance repair'
AND bio = 'Washing machines, ovens, wiring.';

UPDATE worker_profiles SET
    headline_translations = JSON_OBJECT(
        'de', 'Fliesenleger und Maurer',
        'sq', 'Pllakashtrues dhe murator',
        'en', headline
    ),
    bio_translations = JSON_OBJECT(
        'de', 'Badezimmer, Küchen und Terrassen.',
        'sq', 'Banja, kuzhina dhe tarraca.',
        'en', bio
    )
WHERE headline = 'Tiler & mason'
AND bio = 'Bathrooms, kitchens, terraces.';


-- Reviews

UPDATE reviews SET
    review_text_translations = JSON_OBJECT(
        'de', 'Besnik war schnell und hat sehr sauber gearbeitet. Der Wasserhahn funktioniert perfekt.',
        'sq', 'Besniku ishte i shpejtë dhe punoi shumë pastër. Rubineti funksionon në mënyrë perfekte.',
        'en', review_text
    )
WHERE review_text = 'Besnik was fast and very tidy, faucet works perfectly.';

UPDATE reviews SET
    review_text_translations = JSON_OBJECT(
        'de', 'Die Maschine wurde repariert. Es dauerte etwas länger als versprochen, aber der Preis war fair.',
        'sq', 'Pajisja u riparua. Zgjati pak më shumë se sa ishte premtuar, por çmimi ishte i drejtë.',
        'en', review_text
    )
WHERE review_text = 'Machine fixed, took a bit longer than promised but fair price.';

UPDATE reviews SET
    review_text_translations = JSON_OBJECT(
        'de', 'Tolle Arbeit, sehr empfehlenswert!',
        'sq', 'Punë e shkëlqyer, e rekomandoj shumë!',
        'en', review_text
    )
WHERE review_text = 'Great work, highly recommended!';

COMMIT;