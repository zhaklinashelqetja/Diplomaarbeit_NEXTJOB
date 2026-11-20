
import { API_URL } from '$lib/api.js';
import { redirect, fail } from '@sveltejs/kit';

const ADMIN_EMAIL = 'admin@nextjob.al';

const emptyData = {
	users: [],
	jobs: [],
	error: null
};

function readList(payload, keys) {
	if (Array.isArray(payload)) return payload;

	for (const key of keys) {
		if (Array.isArray(payload?.[key])) return payload[key];
		if (Array.isArray(payload?.data?.[key])) return payload.data[key];
	}

	if (Array.isArray(payload?.data)) return payload.data;

	return [];
}

async function apiRequest(fetch, endpoint, token, options = {}) {
	const response = await fetch(`${API_URL}${endpoint}`, {
		...options,
		headers: {
			Accept: 'application/json',
			Authorization: `Bearer ${token}`,
			...(options.body ? { 'Content-Type': 'application/json' } : {}),
			...options.headers
		}
	});

	const text = await response.text();

	let payload = null;

	try {
		payload = text ? JSON.parse(text) : null;
	} catch {
		payload = text;
	}

	if (!response.ok) {
		throw new Error(
			payload?.message ||
				payload?.error ||
				(typeof payload === 'string' ? payload : '') ||
				`API Fehler ${response.status}`
		);
	}

	return payload;
}

async function requireAdmin(fetch, cookies) {
	const token = cookies.get('token');

	if (!token) {
		throw redirect(303, '/login');
	}

	let authData;

	try {
		authData = await apiRequest(fetch, '/api/auth/me', token);
	} catch {
		cookies.delete('token', { path: '/' });
		throw redirect(303, '/login');
	}

	const user = authData?.user ?? authData;

	if (
		!user?.is_admin ||
		user.email?.toLowerCase() !== ADMIN_EMAIL
	) {
		throw redirect(303, '/');
	}

	return token;
}

export async function load({ fetch, cookies }) {
	const token = await requireAdmin(fetch, cookies);

	const [usersResult, jobsResult] = await Promise.allSettled([
		apiRequest(fetch, '/api/admin/users', token),
		apiRequest(fetch, '/api/admin/problems', token)
	]);

	const users =
		usersResult.status === 'fulfilled'
			? readList(usersResult.value, ['users', 'items', 'results'])
			: [];

	const jobs =
		jobsResult.status === 'fulfilled'
			? readList(jobsResult.value, ['problems', 'jobs', 'items', 'results'])
			: [];

	const errors = [];

	if (usersResult.status === 'rejected') {
		errors.push(
			`Benutzer konnten nicht geladen werden: ${usersResult.reason?.message}`
		);
	}

	if (jobsResult.status === 'rejected') {
		errors.push(
			`Jobs konnten nicht geladen werden: ${jobsResult.reason?.message}`
		);
	}

	return {
		users,
		jobs,
		error: errors.length ? errors.join(' | ') : null
	};
}

export const actions = {
	toggleUser: async ({ request, fetch, cookies }) => {
		const token = await requireAdmin(fetch, cookies);
		const formData = await request.formData();

		const id = formData.get('id');
		const isActive = formData.get('isActive') === 'true';

		if (!id) {
			return fail(400, { actionError: 'Benutzer-ID fehlt.' });
		}

		try {
			await apiRequest(fetch, `/api/admin/users/${id}/status`, token, {
				method: 'PATCH',
				body: JSON.stringify({ is_active: !isActive })
			});

			return { success: 'Benutzerstatus wurde geändert.' };
		} catch (error) {
			return fail(500, { actionError: error.message });
		}
	},

	deleteUser: async ({ request, fetch, cookies }) => {
		const token = await requireAdmin(fetch, cookies);
		const formData = await request.formData();

		const id = formData.get('id');

		if (!id) {
			return fail(400, { actionError: 'Benutzer-ID fehlt.' });
		}

		try {
			await apiRequest(fetch, `/api/admin/users/${id}`, token, {
				method: 'DELETE'
			});

			return { success: 'Benutzer wurde gelöscht.' };
		} catch (error) {
			return fail(500, { actionError: error.message });
		}
	},

	updateJob: async ({ request, fetch, cookies }) => {
		const token = await requireAdmin(fetch, cookies);
		const formData = await request.formData();

		const id = formData.get('id');

		if (!id) {
			return fail(400, { actionError: 'Job-ID fehlt.' });
		}

		try {
			await apiRequest(fetch, `/api/admin/problems/${id}`, token, {
				method: 'PUT',
				body: JSON.stringify({
					title: formData.get('title'),
					description: formData.get('description'),
					status: formData.get('status')
				})
			});

			return { success: 'Job wurde aktualisiert.' };
		} catch (error) {
			return fail(500, { actionError: error.message });
		}
	},

	deleteJob: async ({ request, fetch, cookies }) => {
		const token = await requireAdmin(fetch, cookies);
		const formData = await request.formData();

		const id = formData.get('id');

		if (!id) {
			return fail(400, { actionError: 'Job-ID fehlt.' });
		}

		try {
			await apiRequest(fetch, `/api/admin/problems/${id}`, token, {
				method: 'DELETE'
			});

			return { success: 'Job wurde gelöscht.' };
		} catch (error) {
			return fail(500, { actionError: error.message });
		}
	}
};
