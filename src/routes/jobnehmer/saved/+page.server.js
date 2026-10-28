const API_URL = 'http://localhost:5000/api';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    // Prüfen, ob der Benutzer angemeldet ist
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
        const userResponse = await fetch(`${API_URL}/auth/me`, {
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

        const user = await userResponse.json();

        // Gespeicherte Jobs laden
        const savedResponse = await fetch(`${API_URL}/saved`, {
            headers
        });

        if (!savedResponse.ok) {
            console.error(
                'Fehler beim Laden gespeicherter Jobs:',
                savedResponse.status
            );

            return {
                user,
                savedJobs: [],
                error:
                    savedResponse.status === 404
                        ? 'Der API-Endpunkt für gespeicherte Jobs wurde nicht gefunden.'
                        : 'Deine gespeicherten Jobs konnten nicht geladen werden.'
            };
        }

        const responseData = await savedResponse.json();

        // Verschiedene mögliche Antwortformate der API unterstützen
        let savedJobs = [];

        if (Array.isArray(responseData)) {
            savedJobs = responseData;
        } else if (Array.isArray(responseData.savedJobs)) {
            savedJobs = responseData.savedJobs;
        } else if (Array.isArray(responseData.jobs)) {
            savedJobs = responseData.jobs;
        } else if (Array.isArray(responseData.items)) {
            savedJobs = responseData.items;
        }

        return {
            user,
            savedJobs,
            error: null
        };
    } catch (error) {
        console.error('Fehler beim Laden der gespeicherten Jobs:', error);

        return {
            user: null,
            savedJobs: [],
            error: 'Der Server ist momentan nicht erreichbar.'
        };
    }
}
