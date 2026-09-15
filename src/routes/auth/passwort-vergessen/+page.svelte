<script>
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
			const res = await fetch('http://localhost:5000/api/auth/forgot-password', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email })
			});

			const data = await res.json();

			if (!res.ok) {
				error = data.error ?? 'Es ist ein Fehler aufgetreten.';
				return;
			}

			success = 'Eine E-Mail zum Zurücksetzen des Passworts wurde gesendet.';
			email = '';
		} catch {
			error = 'Der Server ist momentan nicht erreichbar.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Passwort vergessen | NextJob</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-2xl font-bold text-gray-900">Passwort vergessen</h1>

	<p class="mt-3 text-gray-600">
		Gib deine E-Mail-Adresse ein. Du erhältst einen Link, mit dem du dein Passwort zurücksetzen
		kannst.
	</p>

	<form onsubmit={forgotPassword} class="mt-6 flex flex-col gap-4">
		<input
			type="email"
			bind:value={email}
			placeholder="E-Mail-Adresse"
			required
			class="rounded-lg border border-gray-300 px-3 py-2"
		/>

		{#if error}
			<p class="text-sm text-red-600">
				{error}
			</p>
		{/if}

		{#if success}
			<p class="text-sm text-green-700">
				{success}
			</p>
		{/if}

		<button
			type="submit"
			disabled={loading}
			class="rounded-lg bg-gray-900 px-4 py-2 font-medium text-white hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
		>
			{loading ? 'Wird gesendet...' : 'Link senden'}
		</button>
	</form>
</div>
