import { API_URL } from '$lib/api.js';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    if (!token) {
        return {
            user: null,
            jobs: [],
            savedJobs: [],
            pageSize: 6,
            error: 'Bitte zuerst einloggen.'
        };
    }

    const headers = {
        Authorization: `Bearer ${token}`
    };

    try {
        // Aktuellen Benutzer laden
        const userResponse = await fetch(`${API_URL}/api/auth/me`, {
            headers
        });

        if (userResponse.status === 401) {
            return {
                user: null,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Die Anmeldung ist nicht mehr gültig. Bitte erneut einloggen.'
            };
        }

        if (!userResponse.ok) {
            console.error(
                'Benutzer konnte nicht geladen werden:',
                userResponse.status
            );

            return {
                user: null,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Deine Benutzerdaten konnten nicht geladen werden.'
            };
        }

        const userData = await userResponse.json();
        const user = userData.user ?? userData;

        // Personalisierte Jobliste laden
        const feedResponse = await fetch(
            `${API_URL}/api/workers/me/feed`,
            { headers }
        );

        if (feedResponse.status === 401) {
            return {
                user,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Die Anmeldung ist nicht mehr gültig. Bitte erneut einloggen.'
            };
        }

        if (!feedResponse.ok) {
            console.error(
                'Feed konnte nicht geladen werden:',
                feedResponse.status,
                feedResponse.statusText
            );

            return {
                user,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Die Aufträge konnten nicht geladen werden.'
            };
        }

        const feedData = await feedResponse.json();

        // API kann direkt ein Array oder ein Objekt liefern
        const result = Array.isArray(feedData)
            ? feedData
            : feedData.jobs ?? feedData.items ?? feedData.problems ?? feedData.feed ?? [];

        const jobs = Array.isArray(result) ? result : [];

        return {
            user,
            jobs,
            savedJobs: [],
            pageSize: 6,
            error: null
        };
    } catch (error) {
        console.error('Jobnehmer-Hauptseite:', error);

        return {
            user: null,
            jobs: [],
            savedJobs: [],
            pageSize: 6,
            error: 'Die Verbindung zum Server konnte nicht hergestellt werden.'
        };
    }
}