
import { writable } from 'svelte/store';
import { API_URL } from '$lib/api.js';

export const isLoggedIn = writable(false);
export const currentUser = writable(null);
export const authLoading = writable(false);

export function checkLogin() {
	if (typeof localStorage === 'undefined') return;

	const token = localStorage.getItem('token');
	isLoggedIn.set(Boolean(token));

	if (!token) {
		currentUser.set(null);
		return;
	}

	loadCurrentUser();
}

export async function loadCurrentUser() {
	if (typeof localStorage === 'undefined') return null;

	const token = localStorage.getItem('token');

	if (!token) {
		isLoggedIn.set(false);
		currentUser.set(null);
		return null;
	}

	authLoading.set(true);

	try {
		const res = await fetch(`${API_URL}/api/auth/me`, {
			headers: {
				Authorization: `Bearer ${token}`
			}
		});

		if (res.status === 401) {
			logout();
			return null;
		}

		if (!res.ok) {
			return null;
		}

		const data = await res.json();
		const user = data.user ?? data;

		currentUser.set(user);
		isLoggedIn.set(true);

		return user;
	} catch (error) {
		console.error('Benutzerdaten konnten nicht geladen werden:', error);
		return null;
	} finally {
		authLoading.set(false);
	}
}

export function logout() {
	if (typeof localStorage !== 'undefined') {
		localStorage.removeItem('token');
	}

	isLoggedIn.set(false);
	currentUser.set(null);
}
