import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';
import { API_URL, localizedUrl } from '$lib/api.js';
import * as m from '$lib/paraglide/messages.js';

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

async function apiRequest(fetch, endpoint, token) {
    const response = await fetch(
        localizedUrl(`${API_URL}${endpoint}`),
        {
            credentials: 'include',
            headers: {
                Accept: 'application/json',
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            m.admin_manage_api_error({ status: response.status })
        );
    }

    return response.json();
}

export async function load({ fetch }) {
    if (!browser) return emptyData;

    const token = localStorage.getItem('token');

    if (!token) {
        throw redirect(302, '/auth/login');
    }

    const authResponse = await fetch(`${API_URL}/api/auth/me`, {
        credentials: 'include',
        headers: {
            Authorization: `Bearer ${token}`
        }
    });

    if (authResponse.status === 401) {
        localStorage.removeItem('token');
        throw redirect(302, '/auth/login');
    }

    if (!authResponse.ok) {
        return {
            ...emptyData,
            error: m.admin_manage_api_error({
                status: authResponse.status
            })
        };
    }

    const authData = await authResponse.json();
    const user = authData.user ?? authData;

    if (!user?.is_admin) {
        throw redirect(302, '/');
    }

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
            m.admin_manage_users_load_failed({
                error: usersResult.reason?.message
            })
        );
    }

    if (jobsResult.status === 'rejected') {
        errors.push(
            m.admin_manage_jobs_load_failed({
                error: jobsResult.reason?.message
            })
        );
    }

    return {
        users,
        jobs,
        error: errors.length ? errors.join(' | ') : null
    };
}
