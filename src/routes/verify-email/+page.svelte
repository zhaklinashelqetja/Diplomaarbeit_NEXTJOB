
<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';
	import { loadCurrentUser } from '$lib/auth.js';

	let loading = $state(true);
	let success = $state(false);
	let message = $state('');

	onMount(() => {
		let cancelled = false;

		async function verifyEmail() {
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

				if (cancelled) return;

				if (!res.ok) {
					message = data.error || 'Die Verifizierung ist fehlgeschlagen.';
					return;
				}

				// Benutzerstatus nach erfolgreicher Verifizierung aktualisieren
				if (localStorage.getItem('token')) {
					await loadCurrentUser();
				}

				if (cancelled) return;

				success = true;
				message = 'Dein Konto wurde erfolgreich verifiziert.';
			} catch {
				if (!cancelled) {
					message = 'Verbindung zum Server nicht möglich.';
				}
			} finally {
				if (!cancelled) {
					loading = false;
				}
			}
		}

		verifyEmail();

		return () => {
			cancelled = true;
		};
	});
</script>

<svelte:head>
	<title>E-Mail verifizieren | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<h1 class="text-3xl font-bold text-[#2A2E38]">
			E-Mail-Verifizierung
		</h1>

		{#if loading}
			<div class="mt-6">
				<p role="status" class="text-[#2A2E38]/70">
					Deine E-Mail-Adresse wird überprüft...
				</p>
			</div>
		{:else if success}
			<div class="mt-6">
				<div class="text-4xl text-[#62AA97]">✓</div>

				<p role="status" class="mt-3 text-[#2A2E38]">
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
				<p role="alert" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
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
