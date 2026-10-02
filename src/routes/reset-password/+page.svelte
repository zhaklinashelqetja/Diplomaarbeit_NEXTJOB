<script>
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';

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
			const res = await fetch(`${API_URL}/api/auth/reset-password`, {
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
				error = data.error || 'Das Passwort konnte nicht geändert werden.';
				return;
			}

			success = 'Dein Passwort wurde erfolgreich geändert.';
			password = '';
			confirmPassword = '';
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Passwort zurücksetzen | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<h1 class="text-3xl font-bold text-[#2A2E38]">Neues Passwort</h1>

		<p class="mt-2 text-sm text-[#2A2E38]/60">
			Erstelle ein neues Passwort für dein NextJob-Konto.
		</p>

		<form onsubmit={resetPassword} class="mt-6 flex flex-col gap-4">
			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-[#2A2E38]">
					Neues Passwort
				</label>

				<input
					id="password"
					type="password"
					bind:value={password}
					placeholder="Neues Passwort"
					required
					minlength="8"
					autocomplete="new-password"
					class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
				/>

				<p class="mt-1 text-xs text-[#2A2E38]/50">Mindestens 8 Zeichen.</p>
			</div>

			<div>
				<label for="confirmPassword" class="mb-1 block text-sm font-medium text-[#2A2E38]">
					Passwort bestätigen
				</label>

				<input
					id="confirmPassword"
					type="password"
					bind:value={confirmPassword}
					placeholder="Passwort bestätigen"
					required
					minlength="8"
					autocomplete="new-password"
					class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
				/>
			</div>

			{#if error}
				<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
					{error}
				</p>
			{/if}

			{#if success}
				<div class="rounded-lg bg-[#62AA97]/10 px-3 py-3">
					<p class="text-sm text-[#2A2E38]">
						{success}
					</p>

					<a
						href={resolve('/auth/login')}
						class="mt-2 inline-block text-sm font-semibold text-[#62AA97] hover:underline"
					>
						Zum Login →
					</a>
				</div>
			{/if}

			<button
				type="submit"
				disabled={loading || success}
				class="rounded-lg bg-[#8FB0C4] px-4 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
			>
				{loading ? 'Wird gespeichert...' : 'Passwort ändern'}
			</button>
		</form>
	</div>
</section>
