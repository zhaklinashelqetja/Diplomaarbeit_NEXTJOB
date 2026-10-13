const API_URL = 'http://localhost:5000/api';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    if (!token) {
        return {
            user: null,
            error: 'Bitte melde dich an, um dein Profil zu sehen.'
        };
    }

    try {
        const response = await fetch(`${API_URL}/auth/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            return {
                user: null,
                error:
                    response.status === 401
                        ? 'Deine Anmeldung ist nicht mehr gültig.'
                        : 'Dein Profil konnte nicht geladen werden.'
            };
        }

        const user = await response.json();

        return {
            user,
            error: null
        };
    } catch (error) {
        console.error('Profil konnte nicht geladen werden:', error);

        return {
            user: null,
            error: 'Der Server ist momentan nicht erreichbar.'
        };
    }
}