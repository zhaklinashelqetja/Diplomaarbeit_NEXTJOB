<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';

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
			const res = await fetch('http://localhost:5000/api/auth/verify', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ token })
			});

			const data = await res.json();

			if (!res.ok) {
				message = data.error ?? 'Die Verifizierung ist fehlgeschlagen.';
				return;
			}

			success = true;
			message = 'Dein Konto wurde erfolgreich verifiziert.';
		} catch {
			message = 'Der Server ist momentan nicht erreichbar.';
		} finally {
			loading = false;
		}
	});
</script>

<svelte:head>
	<title>E-Mail verifizieren | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<h1 class="text-3xl font-bold text-gray-900">E-Mail-Verifizierung</h1>

	{#if loading}
		<p class="mt-6 text-gray-600">Deine E-Mail-Adresse wird überprüft...</p>
	{:else if success}
		<p class="mt-6 text-green-700">{message}</p>

		<a
			href={resolve('/auth/login')}
			class="mt-8 inline-block rounded-lg bg-gray-900 px-5 py-3 font-medium text-white hover:bg-gray-700"
		>
			Zum Login
		</a>
	{:else}
		<p class="mt-6 text-red-600">{message}</p>

		<a
			href={resolve('/auth/verifizierung')}
			class="mt-8 inline-block text-gray-700 underline hover:text-gray-900"
		>
			Zurück
		</a>
	{/if}
</section>
