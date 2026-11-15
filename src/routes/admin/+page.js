
import { browser } from '$app/environment';
import { API_URL } from '$lib/api';

const emptyStats = {
    totalUsers: 0,
    activeJobs: 0,
    totalOffers: 0,
    reportedContent: 0
};

export async function load({ fetch }) {
    const emptyData = {
        stats: emptyStats,
        categoryDemand: [],
        topSearches: [],
        registrationGrowth: [],
        topProblems: [],
        topWorkers: []
    };

    if (!browser) {
        return emptyData;
    }

    const token = localStorage.getItem('token');

    if (!token) {
        return {
            ...emptyData,
            error: 'Nicht angemeldet'
        };
    }

    try {
        const response = await fetch(`${API_URL}/api/admin/stats`, {
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
                error: `API Fehler: ${response.status}`
            };
        }

        const apiData = await response.json();

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
        console.error('Admin API error:', error);

        return {
            ...emptyData,
            error: 'Verbindung zum Server fehlgeschlagen'
        };
    }
}
