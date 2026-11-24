
import { browser } from '$app/environment';
import { redirect } from '@sveltejs/kit';
import { API_URL, localizedUrl } from '$lib/api.js';
import * as m from '$lib/paraglide/messages.js';

const emptyStats = {
    totalUsers: 0,
    activeJobs: 0,
    totalOffers: 0,
    reportedContent: 0
};

const emptyData = {
    stats: emptyStats,
    categoryDemand: [],
    topSearches: [],
    registrationGrowth: [],
    topProblems: [],
    topWorkers: []
};

export async function load({ fetch }) {
    if (!browser) {
        return emptyData;
    }

    const token = localStorage.getItem('token');

    if (!token) {
        throw redirect(302, '/auth/login');
    }

    try {
        // Angemeldeten Benutzer überprüfen
        const authResponse = await fetch(`${API_URL}/api/auth/me`, {
            credentials: 'include',
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!authResponse.ok) {
            localStorage.removeItem('token');
            throw redirect(302, '/auth/login');
        }

        const authData = await authResponse.json();
        const user = authData.user ?? authData;

        // Nur das festgelegte Admin-Konto darf das Dashboard öffnen
        if (
            !user.is_admin ||
            user.email?.toLowerCase() !== 'admin@nextjob.al'
        ) {
            throw redirect(302, '/');
        }

        // Statistiken abrufen
        const response = await fetch(localizedUrl(`${API_URL}/api/admin/stats`), {
            credentials: 'include',
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            console.error(
                'Admin API error:',
                response.status,
                response.statusText
            );

            return {
                ...emptyData,
                error: m.admin_dashboard_api_error({ status: response.status })
            };
        }

        const apiData = await response.json();

        console.log('Admin statistics:', apiData);

        return {
            stats: {
                totalUsers: apiData.total_users ?? 0,
                activeJobs: apiData.active_jobs ?? 0,
                totalOffers: apiData.total_offers ?? 0,
                reportedContent: apiData.reported_content ?? 0
            },
            categoryDemand: apiData.category_demand ?? [],
            topSearches: apiData.top_searches ?? [],
            registrationGrowth: apiData.registration_growth ?? [],
            topProblems: apiData.top_problems ?? [],
            topWorkers: apiData.top_workers ?? []
        };

    } catch (error) {
        if (error?.status === 302) {
            throw error;
        }

        console.error('Admin API error:', error);

        return {
            ...emptyData,
            error: m.admin_dashboard_connection_failed()
        };
    }
}
