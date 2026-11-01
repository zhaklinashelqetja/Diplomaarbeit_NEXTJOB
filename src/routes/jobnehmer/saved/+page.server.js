import { API_URL } from '$lib/api.js';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    if (!token) {
        return {
            user: null,
            savedJobs: [],
            error: 'Bitte melde dich an, um deine gespeicherten Jobs zu sehen.'
        };
    }

    const headers = {
        Authorization: `Bearer ${token}`
    };

    try {
        // Benutzerprofil laden
        const userResponse = await fetch(`${API_URL}/api/auth/me`, {
            headers
        });

        if (!userResponse.ok) {
            return {
                user: null,
                savedJobs: [],
                error:
                    userResponse.status === 401
                        ? 'Deine Anmeldung ist abgelaufen. Bitte melde dich erneut an.'
                        : 'Dein Benutzerprofil konnte nicht geladen werden.'
            };
        }

        const userData = await userResponse.json();
        const user = userData.user ?? userData;

        // Gespeicherte Jobs laden
        const savedResponse = await fetch(
            `${API_URL}/api/workers/me/saved-problems`,
            { headers }
        );

        if (!savedResponse.ok) {
            console.error(
                'Fehler beim Laden gespeicherter Jobs:',
                savedResponse.status,
                savedResponse.statusText
            );

            return {
                user,
                savedJobs: [],
                error:
                    savedResponse.status === 401
                        ? 'Deine Anmeldung ist abgelaufen. Bitte melde dich erneut an.'
                        : 'Deine gespeicherten Jobs konnten nicht geladen werden.'
            };
        }

        const responseData = await savedResponse.json();

        // Verschiedene mögliche Antwortformate unterstützen
        const result = Array.isArray(responseData)
            ? responseData
            : responseData.savedJobs ??
              responseData.saved_jobs ??
              responseData.jobs ??
              responseData.items ??
              responseData.problems ??
              [];

        const savedJobs = Array.isArray(result) ? result : [];

        return {
            user,
            savedJobs,
            error: null
        };
    } catch (error) {
        console.error(
            'Fehler beim Laden der gespeicherten Jobs:',
            error
        );

        return {
            user: null,
            savedJobs: [],
            error: 'Der Server ist momentan nicht erreichbar.'
        };
    }
}