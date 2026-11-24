
import { browser } from '$app/environment';
import { API_URL, localizedUrl } from '$lib/api.js';

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
        const userResponse = await fetch(localizedUrl(`${API_URL}/api/auth/me`), {
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

        // Personalisierte Aufträge laden
        const feedResponse = await fetch(
            localizedUrl(`${API_URL}/api/workers/me/feed`),
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

        let jobs = [];

        // Personalisierter Feed erfolgreich laden
        if (feedResponse.ok) {
            const feedData = await feedResponse.json();

            const result = Array.isArray(feedData)
                ? feedData
                : feedData.jobs ??
                  feedData.items ??
                  feedData.problems ??
                  feedData.feed ??
                  [];

            jobs = Array.isArray(result) ? result : [];
        }

        // Fallback: Allgemeine Aufträge laden, wenn der Feed leer ist
        if (jobs.length === 0) {
            const fallbackResponse = await fetch(
                localizedUrl(`${API_URL}/api/problems`),
                { headers }
            );

            if (fallbackResponse.status === 401) {
                return {
                    user,
                    jobs: [],
                    savedJobs: [],
                    pageSize: 6,
                    error: 'Die Anmeldung ist nicht mehr gültig. Bitte erneut einloggen.'
                };
            }

            if (!fallbackResponse.ok) {
                return {
                    user,
                    jobs: [],
                    savedJobs: [],
                    pageSize: 6,
                    error: 'Die Aufträge konnten nicht geladen werden.'
                };
            }

            const fallbackData = await fallbackResponse.json();

            const result = Array.isArray(fallbackData)
                ? fallbackData
                : fallbackData.jobs ??
                  fallbackData.items ??
                  fallbackData.problems ??
                  fallbackData.feed ??
                  [];

            jobs = Array.isArray(result) ? result : [];
        }

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
