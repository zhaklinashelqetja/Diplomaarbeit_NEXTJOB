import { fail } from '@sveltejs/kit';
import { API_URL } from '$lib/api.js';

async function apiRequest(fetch, token, path, options = {}) {
    return fetch(`${API_URL}${path}`, {
        ...options,
        headers: {
            Authorization: `Bearer ${token}`,
            ...(options.body ? { 'Content-Type': 'application/json' } : {}),
            ...options.headers
        }
    });
}

async function readList(response) {
    const payload = await response.json();

    if (Array.isArray(payload)) return payload;
    if (Array.isArray(payload.users)) return payload.users;
    if (Array.isArray(payload.problems)) return payload.problems;
    if (Array.isArray(payload.jobs)) return payload.jobs;
    if (Array.isArray(payload.items)) return payload.items;
    if (Array.isArray(payload.data)) return payload.data;

    return [];
}

async function getErrorMessage(response) {
    try {
        const payload = await response.json();
        return payload.message ?? payload.error ?? `API-Fehler ${response.status}`;
    } catch {
        return `API-Fehler ${response.status}`;
    }
}

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    if (!token) {
        return {
            users: [],
            jobs: [],
            error: 'Bitte melde dich zuerst mit deinem Admin-Konto an.'
        };
    }

    try {
        const [usersResponse, jobsResponse] = await Promise.all([
            apiRequest(fetch, token, '/api/admin/users'),
            apiRequest(fetch, token, '/api/admin/problems')
        ]);

        const errors = [];

        let users = [];
        let jobs = [];

        if (usersResponse.ok) {
            users = await readList(usersResponse);
        } else {
            errors.push(
                `Nutzer konnten nicht geladen werden: ${await getErrorMessage(usersResponse)}`
            );
        }

        if (jobsResponse.ok) {
            jobs = await readList(jobsResponse);
        } else {
            errors.push(
                `Aufträge konnten nicht geladen werden: ${await getErrorMessage(jobsResponse)}`
            );
        }

        return {
            users,
            jobs,
            error: errors.length ? errors.join(' ') : null
        };
    } catch (error) {
        console.error('Admin-Verwaltung:', error);

        return {
            users: [],
            jobs: [],
            error: 'Der Backend-Server ist nicht erreichbar.'
        };
    }
}

export const actions = {
    toggleUser: async ({ request, fetch, cookies }) => {
        const token = cookies.get('token');

        if (!token) {
            return fail(401, { actionError: 'Bitte melde dich erneut an.' });
        }

        const formData = await request.formData();
        const userId = formData.get('userId')?.toString();
        const isActive = formData.get('isActive') === 'true';

        if (!userId) {
            return fail(400, { actionError: 'Die Nutzer-ID fehlt.' });
        }

        try {
            const response = await apiRequest(
                fetch,
                token,
                `/api/admin/users/${encodeURIComponent(userId)}/status`,
                {
                    method: 'PATCH',
                    body: JSON.stringify({ is_active: !isActive })
                }
            );

            if (!response.ok) {
                return fail(response.status, {
                    actionError: `Nutzerstatus konnte nicht geändert werden: ${await getErrorMessage(response)}`
                });
            }

            return {
                success: true,
                message: !isActive
                    ? 'Nutzer wurde aktiviert.'
                    : 'Nutzer wurde gesperrt.'
            };
        } catch {
            return fail(500, {
                actionError: 'Der Server ist nicht erreichbar.'
            });
        }
    },

    deleteUser: async ({ request, fetch, cookies }) => {
        const token = cookies.get('token');

        if (!token) {
            return fail(401, { actionError: 'Bitte melde dich erneut an.' });
        }

        const formData = await request.formData();
        const userId = formData.get('userId')?.toString();

        if (!userId) {
            return fail(400, { actionError: 'Die Nutzer-ID fehlt.' });
        }

        try {
            const response = await apiRequest(
                fetch,
                token,
                `/api/admin/users/${encodeURIComponent(userId)}`,
                { method: 'DELETE' }
            );

            if (!response.ok) {
                return fail(response.status, {
                    actionError: `Nutzer konnte nicht gelöscht werden: ${await getErrorMessage(response)}`
                });
            }

            return { success: true, message: 'Nutzer wurde gelöscht.' };
        } catch {
            return fail(500, {
                actionError: 'Der Server ist nicht erreichbar.'
            });
        }
    },

    updateJob: async ({ request, fetch, cookies }) => {
        const token = cookies.get('token');

        if (!token) {
            return fail(401, { actionError: 'Bitte melde dich erneut an.' });
        }

        const formData = await request.formData();
        const jobId = formData.get('jobId')?.toString();
        const title = formData.get('title')?.toString().trim();
        const description = formData.get('description')?.toString().trim();
        const status = formData.get('status')?.toString();

        if (!jobId || !title || !description) {
            return fail(400, {
                actionError: 'Bitte fülle Titel und Beschreibung aus.'
            });
        }

        try {
            const response = await apiRequest(
                fetch,
                token,
                `/api/admin/problems/${encodeURIComponent(jobId)}`,
                {
                    method: 'PUT',
                    body: JSON.stringify({ title, description, status })
                }
            );

            if (!response.ok) {
                return fail(response.status, {
                    actionError: `Auftrag konnte nicht aktualisiert werden: ${await getErrorMessage(response)}`
                });
            }

            return {
                success: true,
                message: 'Auftrag wurde aktualisiert.'
            };
        } catch {
            return fail(500, {
                actionError: 'Der Server ist nicht erreichbar.'
            });
        }
    },

    deleteJob: async ({ request, fetch, cookies }) => {
        const token = cookies.get('token');

        if (!token) {
            return fail(401, { actionError: 'Bitte melde dich erneut an.' });
        }

        const formData = await request.formData();
        const jobId = formData.get('jobId')?.toString();

        if (!jobId) {
            return fail(400, { actionError: 'Die Auftrags-ID fehlt.' });
        }

        try {
            const response = await apiRequest(
                fetch,
                token,
                `/api/admin/problems/${encodeURIComponent(jobId)}`,
                { method: 'DELETE' }
            );

            if (!response.ok) {
                return fail(response.status, {
                    actionError: `Auftrag konnte nicht gelöscht werden: ${await getErrorMessage(response)}`
                });
            }

            return { success: true, message: 'Auftrag wurde gelöscht.' };
        } catch {
            return fail(500, {
                actionError: 'Der Server ist nicht erreichbar.'
            });
        }
    }
};