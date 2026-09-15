<script>
	import { page } from '$app/state';
	import { resolve } from '$app/paths';

	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	async function resetPassword(e) {
		e.preventDefault();

		error = '';
		success = '';

		if (password !== confirmPassword) {
			error = 'Die Passwörter stimmen nicht überein.';
			return;
		}

		if (password.length < 8) {
			error = 'Das Passwort muss mindestens 8 Zeichen lang sein.';
			return;
		}

		const token = page.url.searchParams.get('token');

		if (!token) {
			error = 'Der Link zum Zurücksetzen ist ungültig.';
			return;
		}

		loading = true;

		try {
			const res = await fetch('http://localhost:5000/api/auth/reset-password', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					token,
					password
				})
			});

			const data = await res.json();

			if (!res.ok) {
				error = data.error ?? 'Das Passwort konnte nicht geändert werden.';
				return;
			}

			success = 'Dein Passwort wurde erfolgreich geändert.';
			password = '';
			confirmPassword = '';
		} catch {
			error = 'Der Server ist momentan nicht erreichbar.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Passwort zurücksetzen | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16">
	<h1 class="text-3xl font-bold text-gray-900">Neues Passwort</h1>

	<p class="mt-3 text-gray-600">Erstelle ein neues Passwort für dein NextJob-Konto.</p>

	<form onsubmit={resetPassword} class="mt-6 flex flex-col gap-4">
		<input
			type="password"
			bind:value={password}
			placeholder="Neues Passwort"
			required
			class="rounded-lg border border-gray-300 px-3 py-2"
		/>

		<input
			type="password"
			bind:value={confirmPassword}
			placeholder="Passwort bestätigen"
			required
			class="rounded-lg border border-gray-300 px-3 py-2"
		/>

		{#if error}
			<p class="text-sm text-red-600">{error}</p>
		{/if}

		{#if success}
			<p class="text-sm text-green-700">{success}</p>

			<a href={resolve('/auth/login')} class="text-center font-medium text-gray-900 underline">
				Zum Login
			</a>
		{/if}

		<button
			type="submit"
			disabled={loading}
			class="rounded-lg bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700 disabled:opacity-50"
		>
			{loading ? 'Wird gespeichert...' : 'Passwort ändern'}
		</button>
	</form>
</section>
