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
		login_verify_error: 'Ju lutem, konfirmoni fillimisht adresën tuaj të emailit.',
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
		register_role_error: 'Ju lutem, zgjidh si dëshiron ta përdorësh NextJob.',
		register_role_note: 'Zgjedhja aktualisht nuk ruhet.',
		register_email_exists: 'Kjo adresë emaili është tashmë e regjistruar.',
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