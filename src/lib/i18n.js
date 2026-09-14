import { writable, derived } from 'svelte/store';

export const locale = writable('de');

const translations = {
	de: {
		nav_start: 'Start',
		nav_wer_wir_sind: 'Wer wir sind',
		nav_login: 'Login',
		footer_ueber_uns: 'Über uns',
		footer_kontakt: 'Kontakt',
		login_title: 'Anmelden',
		login_email: 'E-Mail',
		login_password: 'Passwort',
		login_button: 'Anmelden',
		register_title: 'Konto erstellen',
		register_firstname: 'Vorname',
		register_lastname: 'Nachname',
		register_email: 'E-Mail',
		register_password: 'Passwort (mind. 8 Zeichen)',
		register_button: 'Registrieren'
	},
	al: {
		nav_start: 'Fillimi',
		nav_wer_wir_sind: 'Kush jemi ne',
		nav_login: 'Hyr',
		footer_ueber_uns: 'Rreth nesh',
		footer_kontakt: 'Kontakti',
		login_title: 'Hyr',
		login_email: 'Email',
		login_password: 'Fjalëkalimi',
		login_button: 'Hyr',
		register_title: 'Krijo llogari',
		register_firstname: 'Emri',
		register_lastname: 'Mbiemri',
		register_email: 'Email',
		register_password: 'Fjalëkalimi (min. 8 shkronja)',
		register_button: 'Regjistrohu'
	}
};

export const t = derived(locale, ($locale) => (key) => translations[$locale][key] ?? key);
