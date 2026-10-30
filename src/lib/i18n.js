import { writable, derived } from 'svelte/store';
import { browser } from '$app/environment';

// Sprache beim Neuladen beibehalten
const savedLocale = browser ? localStorage.getItem('nextjob_locale') : null;

export const locale = writable(
	savedLocale === 'de' || savedLocale === 'al' ? savedLocale : 'de'
);

const translations = {
	de: {
		// NAVIGATION
		nav_start: 'Start',
		nav_jobs: 'Jobs finden',
		nav_chat: 'Chat',
		nav_notifications: 'Benachrichtigungen',
		nav_wer_wir_sind: 'Wer wir sind',
		nav_login: 'Login',
		nav_register: 'Registrieren',
		nav_logout: 'Abmelden',

		// FOOTER
		footer_ueber_uns: 'Über uns',
		footer_kontakt: 'Kontakt',

		// STARTSEITE
		home_badge: 'Lokale Dienstleistungen in Shkodër',
		home_title1: 'Finde Hilfe.',
		home_title2: 'Finde Arbeit.',
		home_description:
			'NextJob bringt Menschen, die Unterstützung brauchen, mit lokalen Dienstleistern und Handwerkern zusammen – einfach, schnell und direkt.',
		home_start: 'Jetzt starten',
		home_more: 'Mehr erfahren',
		home_need_help: 'Ich suche Hilfe',
		home_need_help_desc:
			'Beschreibe deine Aufgabe und erhalte Angebote von passenden lokalen Dienstleistern.',
		home_create_job: 'Auftrag erstellen',
		home_need_work: 'Ich suche Arbeit',
		home_need_work_desc:
			'Entdecke lokale Aufträge, sende dein Angebot und finde neue Kunden in deiner Nähe.',
		home_find_work: 'Arbeit finden',
		home_how: "SO FUNKTIONIERT'S",
		home_steps_title: 'In drei Schritten zum passenden Job',
		home_steps_desc: 'Einfach, schnell und übersichtlich.',
		home_step1: 'Auftrag erstellen',
		home_step1_desc:
			'Beschreibe, welche Arbeit erledigt werden soll und was dir wichtig ist.',
		home_step2: 'Angebote erhalten',
		home_step2_desc:
			'Passende Dienstleister können dein Projekt sehen und dir ein Angebot senden.',
		home_step3: 'Direkt zusammenarbeiten',
		home_step3_desc:
			'Wähle das passende Angebot und kommuniziere direkt über NextJob.',
		home_cta_title: 'Bereit für deinen nächsten Job?',
		home_cta_desc:
			'Erstelle dein NextJob-Konto und werde Teil der lokalen Community.',
		home_cta_button: 'Kostenlos registrieren',

		// LOGIN
		login_title: 'Anmelden',
		login_description: 'Melde dich bei deinem NextJob-Konto an.',
		login_email: 'E-Mail',
		login_password: 'Passwort',
		login_forgot: 'Passwort vergessen?',
		login_button: 'Anmelden',
		login_loading: 'Anmelden...',
		login_no_account: 'Noch kein Konto?',
		login_error: 'E-Mail-Adresse oder Passwort ist falsch.',
		login_email_error: 'E-Mail-Adresse oder Passwort ist falsch.',
		login_verify_error: 'Bitte bestätige zuerst deine E-Mail-Adresse.',
		login_failed: 'Login fehlgeschlagen.',
		login_server_error: 'Verbindung zum Server nicht möglich.',

		// REGISTRIERUNG
		register_title: 'Konto erstellen',
		register_description: 'Erstelle dein NextJob-Konto.',
		register_role_question: 'Wie möchtest du NextJob nutzen?',
		register_worker: 'Jobnehmer',
		register_worker_desc: 'Ich suche Arbeit',
		register_employer: 'Jobgeber',
		register_employer_desc: 'Ich biete Arbeit an',
		register_firstname: 'Vorname',
		register_lastname: 'Nachname',
		register_email: 'E-Mail',
		register_email_hint:
			'Bitte verwende eine E-Mail-Adresse, auf die du Zugriff hast.',
		register_password: 'Passwort (mind. 8 Zeichen)',
		register_password_hint: 'Mindestens 8 Zeichen.',
		register_confirm_password: 'Passwort bestätigen',
		register_repeat_password: 'Passwort wiederholen',
		register_show_password: 'Passwort anzeigen',
		register_password_mismatch: 'Die Passwörter stimmen nicht überein.',
		register_button: 'Registrieren',
		register_loading: 'Wird registriert...',
		register_have_account: 'Du hast bereits ein Konto?',
		register_role_error: 'Bitte wähle aus, wie du NextJob nutzen möchtest.',
		register_role_note: 'Die Auswahl wird derzeit noch nicht gespeichert.',
		register_email_exists: 'Diese E-Mail-Adresse ist bereits registriert.',
		register_failed: 'Registrierung fehlgeschlagen.',

		// PASSWORT VERGESSEN
		forgot_title: 'Passwort vergessen',
		forgot_description:
			'Gib deine E-Mail-Adresse ein. Du erhältst einen Link, mit dem du dein Passwort zurücksetzen kannst.',
		forgot_email_placeholder: 'E-Mail-Adresse',
		forgot_send: 'Link senden',
		forgot_loading: 'Wird gesendet...',
		forgot_success:
			'Eine E-Mail zum Zurücksetzen des Passworts wurde gesendet.',
		forgot_back: 'Zurück zum Login',

		// E-MAIL-VERIFIZIERUNG
		verify_title: 'Überprüfe deine E-Mails',
		verify_description:
			'Wir haben dir eine E-Mail mit einem Verifizierungslink gesendet. Klicke auf den Link, um dein NextJob-Konto zu bestätigen.',
		verify_spam:
			'Überprüfe auch deinen Spam-Ordner, falls du keine E-Mail findest.',
		verify_login: 'Zum Login',

		// WER WIR SIND
		about_title: 'Wer wir sind',
		about_description:
			'NextJob ist eine digitale Plattform, die lokale Dienstleistungen und Handwerker in Shkodra miteinander verbindet.',

		// KONTAKT
		contact_title: 'Kontakt',
		contact_description:
			'Bei Fragen zur NextJob-Plattform kannst du uns gerne kontaktieren.',
		contact_location: 'Standort: Shkodër, Albanien',
		contact_email: 'E-Mail',

		// JOBNEHMER-HAUPTSEITE
		worker_page_title: 'Jobnehmer',
		worker_meta_description: 'Entdecke passende Aufträge auf NextJob.',
		worker_for_you: 'Für dich',
		worker_welcome: 'Willkommen bei NextJob',
		worker_intro:
			'Entdecke passende Aufträge und finde Jobs, die zu deinen Fähigkeiten und deinem Standort passen.',
		worker_search: 'Aufträge suchen',
		worker_search_placeholder: 'z. B. painter, Shkodra ...',
		worker_clear_search: 'Suchtext löschen',
		worker_search_hint:
			'Suche nach Wörtern oder Wortteilen. Leichte Tippfehler werden bei längeren Wörtern berücksichtigt.',
		worker_matching_jobs: 'Passende Aufträge',
		worker_recommendations: 'Empfehlungen für dich',
		worker_urgent: 'Dringend',
		worker_open: 'Offen',
		worker_no_title: 'Ohne Titel',
		worker_no_description: 'Keine Beschreibung vorhanden.',
		worker_view_job: 'Auftrag ansehen',
		worker_pagination: 'Seitennavigation für Aufträge',
		worker_page: 'Seite',
		worker_of: 'von',
		worker_previous: 'Zurück',
		worker_next: 'Weiter',
		worker_no_results: 'Keine passenden Aufträge gefunden',
		worker_no_jobs: 'Aktuell keine Aufträge verfügbar',
		worker_try_again:
			'Versuche einen anderen Suchbegriff oder setze die Suche zurück.',
		worker_check_later:
			'Schau später wieder vorbei. Neue Aufträge können jederzeit hinzukommen.',
		worker_reset: 'Suche zurücksetzen',
		worker_role: 'Jobnehmer',
		worker_view_profile: 'Profil ansehen',
		worker_following: 'Meine Folgen',
		worker_followed_users: 'Gefolgte Nutzer',
		worker_follow_description:
			'Folge interessanten Jobnehmern oder Jobgebern und behalte ihre Aktivitäten im Blick.',
		worker_manage_following: 'Folgen verwalten',
		worker_saved_jobs: 'Gespeicherte Jobs',
		worker_saved_description:
			'Speichere interessante Aufträge, um sie später schnell wiederzufinden.',
		worker_contribution: 'Dein Beitrag',
		worker_contribution_description:
			'Teile deine Erfahrungen und Aktivitäten auf NextJob.',
		worker_open_profile: 'Profil öffnen',

		// KATEGORIEN
		worker_category_all: 'Alle',
		worker_category_Plumber: 'Installateur',
		worker_category_Electrician: 'Elektriker',
		worker_category_Painter: 'Maler',
		worker_category_Carpenter: 'Tischler',
		worker_category_Mason: 'Maurer',
		worker_category_Roofer: 'Dachdecker',
		worker_category_Gardener: 'Gärtner',
		worker_category_Cleaner: 'Reinigungskraft',

		// JOBNEHMER-PROFIL
		profile_title: 'Mein Profil',
		profile_meta_description:
			'Dein persönliches Jobnehmer-Profil auf NextJob.',
		profile_unavailable: 'Profil nicht verfügbar',
		profile_back_to_jobs: 'Zur Jobnehmer-Hauptseite',
		profile_my_area: 'Mein Bereich',
		profile_intro:
			'Präsentiere deine Fähigkeiten und zeige anderen, welche Dienstleistungen du anbietest.',
		profile_initials_of: 'Initialen von',
		profile_discover_jobs: 'Aufträge entdecken',
		profile_about_me: 'Über mich',
		profile_no_bio:
			'Du hast noch keine Beschreibung hinzugefügt. Eine kurze Vorstellung hilft anderen Nutzern, dich und deine Arbeit besser kennenzulernen.',
		profile_my_skills: 'Meine Fähigkeiten',
		profile_no_skills:
			'Es wurden noch keine Fähigkeiten hinterlegt. Hier können beispielsweise handwerkliche Kenntnisse, Design oder Marketing angezeigt werden, sobald sie in deinen Profildaten vorhanden sind.',
		profile_contact_info: 'Kontaktinformationen',
		profile_email: 'E-Mail',
		profile_phone: 'Telefonnummer',
		profile_location: 'Standort',
		profile_no_contact:
			'Es sind noch keine Kontaktinformationen vorhanden.',
		profile_overview: 'Profilübersicht',
		profile_data: 'Profildaten',
		profile_completeness: 'Profilvollständigkeit',
		profile_progress_description:
			'Ein vollständiges Profil hilft anderen Nutzern, deine Fähigkeiten und Angebote besser einzuschätzen.',
		profile_load_failed:
			'Deine Profildaten konnten nicht geladen werden.',

		// GESPEICHERTE JOBS
		saved_title: 'Gespeicherte Jobs',
		saved_meta_description:
			'Finde deine gespeicherten Aufträge auf NextJob wieder.',
		saved_description:
			'Behalte interessante Aufträge im Blick und finde sie später schnell wieder.',
		saved_discover_jobs: 'Aufträge entdecken',
		saved_my_jobs: 'Meine gespeicherten Aufträge',
		saved_status: 'Gespeichert',
		saved_no_id: 'Für diesen Auftrag ist keine ID vorhanden.',
		saved_pagination: 'Seitennavigation',
		saved_empty_title: 'Noch keine Jobs gespeichert',
		saved_empty_description:
			'Wenn du interessante Aufträge findest, kannst du sie speichern und später hier wiederfinden.',

		// CHAT
		chat_title: 'Nachrichten',
		chat_description:
			'Deine Gespräche mit Auftraggebern und Dienstleistern.',
		chat_loading: 'Nachrichten werden geladen...',
		chat_empty: 'Du hast noch keine Nachrichten.',
		chat_back: 'Zurück zu Nachrichten',
		chat_loading_conversation: 'Chat wird geladen...',
		chat_empty_conversation:
			'Noch keine Nachrichten. Schreibe die erste Nachricht.',
		chat_send: 'Senden',
		chat_load_error: 'Nachrichten konnten nicht geladen werden.',
		chat_load_failed: 'Chat konnte nicht geladen werden.',
		chat_send_failed: 'Nachricht konnte nicht gesendet werden.',
		chat_server_error: 'Verbindung zum Server nicht möglich.',
		chat_message_placeholder: 'Nachricht schreiben...',
		chat_sending: 'Wird gesendet...',

		// ADMIN
		admin_title: 'Admin-Dashboard',
		admin_statistics: 'Plattformkennzahlen',
		admin_overview: 'Aktueller Überblick über NextJob',
		admin_users: 'Nutzer',
		admin_registered_users: 'Registrierte Nutzer',
		admin_active_jobs: 'Aktive Jobs',
		admin_current_jobs: 'Aktuell laufende Jobs',
		admin_offers: 'Angebote',
		admin_submitted_offers: 'Eingereichte Angebote',
		admin_reports: 'Gemeldete Inhalte',
		admin_reported_reviews: 'Markierte Bewertungen',
		admin_category_demand: 'Nachfrage nach Kategorien',
		admin_searches: 'Häufigste Suchbegriffe',
		admin_user_growth: 'Nutzerentwicklung',

		// ALLGEMEIN
		common_email: 'E-Mail',
		common_password: 'Passwort',
		common_save: 'Speichern',
		common_cancel: 'Abbrechen',
		common_delete: 'Löschen',
		common_edit: 'Bearbeiten',
		common_back: 'Zurück',
		common_loading: 'Wird geladen...',
		common_error: 'Es ist ein Fehler aufgetreten.',
		common_server_error: 'Verbindung zum Server nicht möglich.',

		// FEHLERSEITE
		error_title: 'Etwas ist schiefgelaufen',
		error_description:
			'Diese Seite existiert nicht oder ist nicht verfügbar.',
		error_back: 'Zurück zur Startseite'
	},

	al: {
		// NAVIGIMI
		nav_start: 'Kreu',
		nav_jobs: 'Gjej punë',
		nav_chat: 'Bisedat',
		nav_notifications: 'Njoftimet',
		nav_wer_wir_sind: 'Kush jemi ne',
		nav_login: 'Hyr',
		nav_register: 'Regjistrohu',
		nav_logout: 'Dil',

		// FOOTER
		footer_ueber_uns: 'Rreth nesh',
		footer_kontakt: 'Kontakt',

		// FAQJA KRYESORE
		home_badge: 'Shërbime lokale në Shkodër',
		home_title1: 'Gjej ndihmë.',
		home_title2: 'Gjej punë.',
		home_description:
			'NextJob lidh njerëzit që kanë nevojë për ndihmë me ofruesit lokalë të shërbimeve dhe zejtarët në Shkodër – thjesht, shpejt dhe drejtpërdrejt.',
		home_start: 'Fillo tani',
		home_more: 'Mëso më shumë',
		home_need_help: 'Kërkoj ndihmë',
		home_need_help_desc:
			'Përshkruaj punën që duhet bërë dhe merr oferta nga ofruesit e përshtatshëm lokalë.',
		home_create_job: 'Krijo një kërkesë',
		home_need_work: 'Kërkoj punë',
		home_need_work_desc:
			'Zbulo punë lokale, dërgo ofertën tënde dhe gjej klientë të rinj pranë teje.',
		home_find_work: 'Gjej punë',
		home_how: 'SI FUNKSIONON',
		home_steps_title: 'Gjej punën e duhur në tre hapa',
		home_steps_desc: 'Thjesht, shpejt dhe qartë.',
		home_step1: 'Krijo një kërkesë',
		home_step1_desc:
			'Përshkruaj punën që duhet kryer dhe çfarë është e rëndësishme për ty.',
		home_step2: 'Merr oferta',
		home_step2_desc:
			'Ofruesit e përshtatshëm të shërbimeve mund ta shohin kërkesën tënde dhe të dërgojnë oferta.',
		home_step3: 'Bashkëpunoni drejtpërdrejt',
		home_step3_desc:
			'Zgjidh ofertën e përshtatshme dhe komuniko drejtpërdrejt përmes NextJob.',
		home_cta_title: 'Gati për punën tënde të radhës?',
		home_cta_desc:
			'Krijo llogarinë tënde në NextJob dhe bëhu pjesë e komunitetit lokal.',
		home_cta_button: 'Regjistrohu falas',

		// HYRJA
		login_title: 'Hyr',
		login_description: 'Hyr në llogarinë tënde NextJob.',
		login_email: 'Email',
		login_password: 'Fjalëkalimi',
		login_forgot: 'Ke harruar fjalëkalimin?',
		login_button: 'Hyr',
		login_loading: 'Duke hyrë...',
		login_no_account: 'Nuk ke ende një llogari?',
		login_error: 'Emaili ose fjalëkalimi është i pasaktë.',
		login_email_error: 'Emaili ose fjalëkalimi është i pasaktë.',
		login_verify_error:
			'Ju lutem, konfirmoni fillimisht adresën tuaj të emailit.',
		login_failed: 'Hyrja dështoi.',
		login_server_error: 'Nuk mund të lidhemi me serverin.',

		// REGJISTRIMI
		register_title: 'Krijo llogari',
		register_description: 'Krijo llogarinë tënde NextJob.',
		register_role_question: 'Si dëshiron ta përdorësh NextJob?',
		register_worker: 'Punëkërkues',
		register_worker_desc: 'Kërkoj punë',
		register_employer: 'Punëdhënës',
		register_employer_desc: 'Ofroj punë',
		register_firstname: 'Emri',
		register_lastname: 'Mbiemri',
		register_email: 'Email',
		register_email_hint:
			'Përdor një adresë emaili në të cilën ke qasje.',
		register_password: 'Fjalëkalimi (min. 8 karaktere)',
		register_password_hint: 'Të paktën 8 karaktere.',
		register_confirm_password: 'Konfirmo fjalëkalimin',
		register_repeat_password: 'Përsërit fjalëkalimin',
		register_show_password: 'Shfaq fjalëkalimin',
		register_password_mismatch: 'Fjalëkalimet nuk përputhen.',
		register_button: 'Regjistrohu',
		register_loading: 'Duke u regjistruar...',
		register_have_account: 'Ke tashmë një llogari?',
		register_role_error:
			'Ju lutem, zgjidh si dëshiron ta përdorësh NextJob.',
		register_role_note: 'Zgjedhja aktualisht nuk ruhet.',
		register_email_exists:
			'Kjo adresë emaili është tashmë e regjistruar.',
		register_failed: 'Regjistrimi dështoi.',

		// FJALËKALIMI I HARRUAR
		forgot_title: 'Ke harruar fjalëkalimin?',
		forgot_description:
			'Shkruaj adresën tënde të emailit. Do të marrësh një lidhje për të rivendosur fjalëkalimin.',
		forgot_email_placeholder: 'Adresa e emailit',
		forgot_send: 'Dërgo lidhjen',
		forgot_loading: 'Duke dërguar...',
		forgot_success:
			'U dërgua një email për rivendosjen e fjalëkalimit.',
		forgot_back: 'Kthehu te hyrja',

		// VERIFIKIMI I EMAILIT
		verify_title: 'Kontrollo emailin tënd',
		verify_description:
			'Të kemi dërguar një email me një lidhje verifikimi. Kliko lidhjen për të konfirmuar llogarinë tënde NextJob.',
		verify_spam:
			'Kontrollo edhe dosjen Spam nëse nuk e gjen emailin.',
		verify_login: 'Shko te hyrja',

		// KUSH JEMI NE
		about_title: 'Kush jemi ne',
		about_description:
			'NextJob është një platformë digjitale që lidh ofruesit e shërbimeve lokale dhe zejtarët në Shkodër me njëri-tjetrin.',

		// KONTAKTI
		contact_title: 'Kontakt',
		contact_description:
			'Nëse ke pyetje rreth platformës NextJob, mund të na kontaktosh.',
		contact_location: 'Vendndodhja: Shkodër, Shqipëri',
		contact_email: 'Email',

		// FAQJA KRYESORE E PUNËKËRKUESIT
		worker_page_title: 'Punëkërkues',
		worker_meta_description: 'Zbulo punët e përshtatshme në NextJob.',
		worker_for_you: 'Për ty',
		worker_welcome: 'Mirë se vjen në NextJob',
		worker_intro:
			'Zbulo punët e përshtatshme dhe gjej mundësi që përputhen me aftësitë dhe vendndodhjen tënde.',
		worker_search: 'Kërko punë',
		worker_search_placeholder: 'p.sh. painter, Shkodra ...',
		worker_clear_search: 'Pastro kërkimin',
		worker_search_hint:
			'Kërko sipas fjalëve ose pjesëve të tyre. Gabimet e vogla të shkrimit tolerohen për fjalët më të gjata.',
		worker_matching_jobs: 'Punë të përshtatshme',
		worker_recommendations: 'Rekomandime për ty',
		worker_urgent: 'Urgjente',
		worker_open: 'E hapur',
		worker_no_title: 'Pa titull',
		worker_no_description: 'Nuk ka përshkrim.',
		worker_view_job: 'Shiko punën',
		worker_pagination: 'Navigimi i faqeve të punëve',
		worker_page: 'Faqja',
		worker_of: 'nga',
		worker_previous: 'Mbrapa',
		worker_next: 'Përpara',
		worker_no_results: 'Nuk u gjetën punë të përshtatshme',
		worker_no_jobs: 'Aktualisht nuk ka punë të disponueshme',
		worker_try_again:
			'Provo një fjalë tjetër kërkimi ose rivendos filtrat.',
		worker_check_later:
			'Kontrollo përsëri më vonë. Punë të reja mund të shtohen në çdo kohë.',
		worker_reset: 'Rivendos filtrat',
		worker_role: 'Punëkërkues',
		worker_view_profile: 'Shiko profilin',
		worker_following: 'Personat që ndjek',
		worker_followed_users: 'Përdoruesit që ndjek',
		worker_follow_description:
			'Ndiq punëkërkues ose punëdhënës interesantë dhe qëndro i informuar për aktivitetet e tyre.',
		worker_manage_following: 'Menaxho ndjekjet',
		worker_saved_jobs: 'Punët e ruajtura',
		worker_saved_description:
			'Ruaj punët që të interesojnë për t’i gjetur lehtësisht më vonë.',
		worker_contribution: 'Kontributi yt',
		worker_contribution_description:
			'Ndaj përvojat dhe aktivitetet e tua në NextJob.',
		worker_open_profile: 'Hap profilin',

		// KATEGORITË
		worker_category_all: 'Të gjitha',
		worker_category_Plumber: 'Hidraulik',
		worker_category_Electrician: 'Elektricist',
		worker_category_Painter: 'Bojaxhi',
		worker_category_Carpenter: 'Marangoz',
		worker_category_Mason: 'Murator',
		worker_category_Roofer: 'Çatipunues',
		worker_category_Gardener: 'Kopshtar',
		worker_category_Cleaner: 'Pastrues',

		// PROFILI I PUNËKËRKUESIT
		profile_title: 'Profili im',
		profile_meta_description:
			'Profili yt personal si punëkërkues në NextJob.',
		profile_unavailable: 'Profili nuk është i disponueshëm',
		profile_back_to_jobs: 'Kthehu te faqja kryesore e punëkërkuesit',
		profile_my_area: 'Hapësira ime',
		profile_intro:
			'Prezanto aftësitë e tua dhe tregoju të tjerëve cilat shërbime ofron.',
		profile_initials_of: 'Inicialet e',
		profile_discover_jobs: 'Zbulo punë',
		profile_about_me: 'Rreth meje',
		profile_no_bio:
			'Nuk ke shtuar ende një përshkrim. Një prezantim i shkurtër i ndihmon përdoruesit e tjerë të të njohin më mirë ty dhe punën tënde.',
		profile_my_skills: 'Aftësitë e mia',
		profile_no_skills:
			'Nuk janë shtuar ende aftësi. Këtu mund të shfaqen, për shembull, aftësi profesionale, dizajn ose marketing, sapo të jenë pjesë e të dhënave të profilit tënd.',
		profile_contact_info: 'Informacionet e kontaktit',
		profile_email: 'Email',
		profile_phone: 'Numri i telefonit',
		profile_location: 'Vendndodhja',
		profile_no_contact:
			'Nuk ka ende informacione kontakti.',
		profile_overview: 'Përmbledhja e profilit',
		profile_data: 'Të dhënat e profilit',
		profile_completeness: 'Plotësimi i profilit',
		profile_progress_description:
			'Një profil i plotë i ndihmon përdoruesit e tjerë të vlerësojnë më mirë aftësitë dhe shërbimet e tua.',
		profile_load_failed:
			'Të dhënat e profilit tënd nuk mund të ngarkoheshin.',

		// PUNËT E RUAJTURA
		saved_title: 'Punët e ruajtura',
		saved_meta_description:
			'Gjej përsëri punët që ke ruajtur në NextJob.',
		saved_description:
			'Mbaji në vëmendje punët që të interesojnë dhe gjeji lehtësisht më vonë.',
		saved_discover_jobs: 'Zbulo punë',
		saved_my_jobs: 'Punët e mia të ruajtura',
		saved_status: 'E ruajtur',
		saved_no_id: 'Kjo punë nuk ka një ID.',
		saved_pagination: 'Navigimi i faqeve',
		saved_empty_title: 'Nuk ke ruajtur ende asnjë punë',
		saved_empty_description:
			'Kur të gjesh punë interesante, mund t’i ruash dhe t’i gjesh përsëri këtu më vonë.',

		// BISEDAT
		chat_title: 'Mesazhet',
		chat_description:
			'Bisedat e tua me klientët dhe ofruesit e shërbimeve.',
		chat_loading: 'Mesazhet po ngarkohen...',
		chat_empty: 'Nuk ke ende mesazhe.',
		chat_back: 'Kthehu te mesazhet',
		chat_loading_conversation: 'Biseda po ngarkohet...',
		chat_empty_conversation:
			'Nuk ka ende mesazhe. Shkruaj mesazhin e parë.',
		chat_send: 'Dërgo',
		chat_load_error: 'Mesazhet nuk mund të ngarkoheshin.',
		chat_load_failed: 'Biseda nuk mund të ngarkohej.',
		chat_send_failed: 'Mesazhi nuk mund të dërgohej.',
		chat_server_error: 'Nuk mund të lidhemi me serverin.',
		chat_message_placeholder: 'Shkruaj një mesazh...',
		chat_sending: 'Duke dërguar...',

		// ADMIN
		admin_title: 'Paneli i administratorit',
		admin_statistics: 'Statistikat e platformës',
		admin_overview: 'Përmbledhje aktuale e NextJob',
		admin_users: 'Përdoruesit',
		admin_registered_users: 'Përdorues të regjistruar',
		admin_active_jobs: 'Punë aktive',
		admin_current_jobs: 'Punë aktualisht aktive',
		admin_offers: 'Ofertat',
		admin_submitted_offers: 'Oferta të dërguara',
		admin_reports: 'Përmbajtje e raportuar',
		admin_reported_reviews: 'Vlerësime të raportuara',
		admin_category_demand: 'Kërkesa sipas kategorive',
		admin_searches: 'Termat më të kërkuar',
		admin_user_growth: 'Rritja e përdoruesve',

		// TË PËRGJITHSHME
		common_email: 'Email',
		common_password: 'Fjalëkalimi',
		common_save: 'Ruaj',
		common_cancel: 'Anulo',
		common_delete: 'Fshi',
		common_edit: 'Ndrysho',
		common_back: 'Kthehu',
		common_loading: 'Duke ngarkuar...',
		common_error: 'Ndodhi një gabim.',
		common_server_error: 'Nuk mund të lidhemi me serverin.',

		// FAQJA E GABIMIT
		error_title: 'Diçka shkoi keq',
		error_description:
			'Kjo faqe nuk ekziston ose nuk është e disponueshme.',
		error_back: 'Kthehu në faqen kryesore'
	}
};

// Sprache speichern
if (browser) {
	locale.subscribe((value) => {
		localStorage.setItem('nextjob_locale', value);
		document.documentElement.lang = value === 'al' ? 'sq' : 'de';
	});
}

// Übersetzungsfunktion
export const t = derived(locale, ($locale) => {
	return (key) => {
		return translations[$locale]?.[key] ?? translations.de[key] ?? key;
	};
});