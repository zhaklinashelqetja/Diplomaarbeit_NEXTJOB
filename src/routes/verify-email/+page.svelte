<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';

	let loading = $state(true);
	let success = $state(false);
	let message = $state('');

	onMount(async () => {
		const token = page.url.searchParams.get('token');

		if (!token) {
			message = 'Der Verifizierungslink ist ungültig.';
			loading = false;
			return;
		}

		try {
			const res = await fetch(`${API_URL}/api/auth/verify`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const data = await res.json();

			if (!res.ok) {
				message = data.error || 'Die Verifizierung ist fehlgeschlagen.';
				return;
			}

			success = true;
			message = 'Dein Konto wurde erfolgreich verifiziert.';
		} catch {
			message = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>E-Mail verifizieren | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<h1 class="text-3xl font-bold text-[#2A2E38]">E-Mail-Verifizierung</h1>

		{#if loading}
			<div class="mt-6">
				<p class="text-[#2A2E38]/70">Deine E-Mail-Adresse wird überprüft...</p>
			</div>
		{:else if success}
			<div class="mt-6">
				<div class="text-4xl">✓</div>

				<p class="mt-3 text-[#2A2E38]">
					{message}
				</p>

				<a
					href={resolve('/auth/login')}
					class="mt-8 inline-block rounded-lg bg-[#8FB0C4] px-5 py-3 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
				>
					Zum Login
				</a>
			</div>
		{:else}
			<div class="mt-6">
				<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
					{message}
				</p>

				<a
					href={resolve('/auth/verifizierung')}
					class="mt-6 inline-block font-medium text-[#8FB0C4] hover:text-[#62AA97]"
				>
					← Zurück
				</a>
			</div>
		{/if}
	</div>
</section>
