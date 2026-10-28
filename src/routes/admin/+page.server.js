export async function load({ fetch }) {
    const response = await fetch('http://localhost:5000/api/admin/stats');

    if (!response.ok) {
        console.error('Admin API error:', response.status, response.statusText);

        return {
            stats: {
                totalUsers: 0,
                activeJobs: 0,
                totalOffers: 0,
                reportedContent: 0
            },
            categoryDemand: [],
            topSearches: [],
            registrationGrowth: [],
            topProblems: [],
            topWorkers: [],
            error: `API Fehler: ${response.status}`
        };
    }

    const apiData = await response.json();

    console.log('Admin API:', apiData);

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
}