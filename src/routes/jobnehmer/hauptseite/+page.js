import { browser } from '$app/environment';
import { API_URL } from '$lib/api.js';

export async function load({ fetch }) {
    if (!browser) {
        return {
            user: null,
            jobs: [],
            savedJobs: [],
            pageSize: 6,
            error: null
        };
    }

    const token = localStorage.getItem('token');

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

        // Offene Aufträge für Jobnehmer laden
        const feedResponse = await fetch(
        `${API_URL}/api/problems`,
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

        if (feedResponse.status === 403) {
            return {
                user,
                jobs: [],
                savedJobs: [],
                pageSize: 6,
                error: 'Du benötigst ein Jobnehmer-Profil, um die Aufträge zu sehen.'
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

        const result = Array.isArray(feedData)
            ? feedData
            : feedData.jobs ??
              feedData.items ??
              feedData.problems ??
              feedData.feed ??
              [];

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