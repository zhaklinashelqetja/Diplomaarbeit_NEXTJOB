import { API_URL } from '$lib/api.js';

export async function load({ fetch, cookies }) {
    const token = cookies.get('token');

    if (!token) {
        return {
            user: null,
            error: 'Bitte melde dich an, um dein Profil zu sehen.'
        };
    }

    try {
        const response = await fetch(`${API_URL}/api/auth/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        if (!response.ok) {
            return {
                user: null,
                error:
                    response.status === 401
                        ? 'Deine Anmeldung ist nicht mehr gültig. Bitte melde dich erneut an.'
                        : 'Dein Profil konnte nicht geladen werden.'
            };
        }

        const userData = await response.json();
        const user = userData.user ?? userData;

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