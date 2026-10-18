const API_URL = 'http://localhost:5000/api';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    // Noch nicht eingeloggt
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
        const userResponse = await fetch(`${API_URL}/auth/me`, {
            headers
        });

        if (!userResponse.ok) {
            return {
                user: null,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Die Anmeldung ist nicht mehr gültig.'
            };
        }

        const user = await userResponse.json();

        // For-You-Feed laden
        const feedResponse = await fetch(`${API_URL}/feed`, {
            headers
        });

        let jobs = [];
        let error = null;

        if (feedResponse.ok) {
            const feedData = await feedResponse.json();

            // API kann direkt ein Array oder ein Objekt liefern
            if (Array.isArray(feedData)) {
                jobs = feedData;
            } else {
                const result =
                    feedData.jobs ??
                    feedData.items ??
                    feedData.problems ??
                    [];

                jobs = Array.isArray(result) ? result : [];
            }
        } else {
            console.error(
                'Feed konnte nicht geladen werden:',
                feedResponse.status
            );

            error = 'Die Aufträge konnten nicht geladen werden.';
        }

        return {
            user,
            jobs,
            savedJobs: [],
            pageSize: 6,
            error
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
