import { writable } from 'svelte/store';

export const isLoggedIn = writable(false);

export function checkLogin() {
	if (typeof localStorage !== 'undefined') {
		isLoggedIn.set(Boolean(localStorage.getItem('token')));
	}
}

export function logout() {
	if (typeof localStorage !== 'undefined') {
		localStorage.removeItem('token');
	}

	isLoggedIn.set(false);
}
