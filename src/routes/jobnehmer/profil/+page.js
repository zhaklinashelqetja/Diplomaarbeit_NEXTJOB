import { API_URL } from '$lib/api.js';
import { browser } from '$app/environment';

export async function load({ fetch }) {
    if (!browser) {
        return { user: null, error: null };
    }

    const token = localStorage.getItem('token');

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

        return {
            user: userData.user ?? userData,
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