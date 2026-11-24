const API_URL = 'http://localhost:5000/api';

export async function load({ fetch }) {
    try {
        const response = await fetch(`${API_URL}/leaderboard`);

        if (!response.ok) {
            console.error('Leaderboard API Fehler:', response.status);

            return {
                workers: [],
                employers: [],
                leaderboardAvailable: false
            };
        }

        const result = await response.json();

        return {
            workers: result.workers ?? [],
            employers: result.employers ?? [],
            leaderboardAvailable: true
        };
    } catch (error) {
        console.error('Leaderboard konnte nicht geladen werden:', error);

        return {
            workers: [],
            employers: [],
            leaderboardAvailable: false
        };
    }
}