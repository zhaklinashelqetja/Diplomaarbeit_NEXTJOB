<script>
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';

	let email = $state('');
	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	async function forgotPassword(e) {
		e.preventDefault();

		error = '';
		success = '';
		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/forgot-password`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email })
			});

			const data = await res.json();

			if (!res.ok) {
				error = data.error || 'Es ist ein Fehler aufgetreten.';
				return;
			}

			success = 'Eine E-Mail zum Zurücksetzen des Passworts wurde gesendet.';
			email = '';
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Passwort vergessen | NextJob</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-3xl font-bold text-[#2A2E38]">Passwort vergessen</h1>

	<p class="mt-2 text-sm text-[#2A2E38]/60">
		Gib deine E-Mail-Adresse ein. Du erhältst einen Link, mit dem du dein Passwort zurücksetzen
		kannst.
	</p>

	<form onsubmit={forgotPassword} class="mt-6 flex flex-col gap-4">
		<div>
			<label for="email" class="mb-1 block text-sm font-medium text-[#2A2E38]"> E-Mail </label>

			<input
				id="email"
				type="email"
				bind:value={email}
				placeholder="E-Mail-Adresse"
				required
				autocomplete="email"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
		</div>

		{#if error}
			<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
				{error}
			</p>
		{/if}

		{#if success}
			<p class="rounded-lg bg-[#62AA97]/10 px-3 py-2 text-sm text-[#2A2E38]">
				{success}
			</p>
		{/if}

		<button
			type="submit"
			disabled={loading}
			class="rounded-lg bg-[#8FB0C4] px-4 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
		>
			{loading ? 'Wird gesendet...' : 'Link senden'}
		</button>
	</form>

	<p class="mt-6 text-center text-sm">
		<a href={resolve('/auth/login')} class="font-semibold text-[#8FB0C4] hover:text-[#62AA97]">
			← Zurück zum Login
		</a>
	</p>
</div>
