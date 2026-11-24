import { API_URL } from '$lib/api.js';

const empty = { workers: [], employers: [], leaderboardAvailable: false };

export async function load({ fetch }) {
    try {
        const response = await fetch(`${API_URL}/api/leaderboard`);
        if (!response.ok) return empty;

        const result = await response.json();
        return {
            workers: result.workers ?? [],
            employers: result.employers ?? [],
            leaderboardAvailable: true
        };
    } catch (error) {
        console.error('Leaderboard konnte nicht geladen werden:', error);
        return empty;
    }
}
