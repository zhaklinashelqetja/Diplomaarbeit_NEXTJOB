<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
	import { API_URL } from '$lib/api.js';

	let first_name = $state('');
	let last_name = $state('');
	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function register(e) {
		e.preventDefault();

		error = '';
		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					first_name,
					last_name,
					email,
					password
				})
			});

			const data = await res.json();

			if (!res.ok) {
				if (data.error === 'Email already registered') {
					error = 'Diese E-Mail-Adresse ist bereits registriert.';
				} else {
					error = data.error || 'Registrierung fehlgeschlagen.';
				}

				return;
			}

			// Noch nicht einloggen:
			// Zuerst muss die E-Mail-Adresse bestätigt werden.
			goto(resolve('/auth/verifizierung'));
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Registrieren | NextJob</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-3xl font-bold text-[#2A2E38]">
		{$t('register_title')}
	</h1>

	<p class="mt-2 text-sm text-[#2A2E38]/60">Erstelle dein NextJob-Konto.</p>

	<form onsubmit={register} class="mt-6 flex flex-col gap-4">
		<div>
			<label for="first_name" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				Vorname
			</label>

			<input
				id="first_name"
				type="text"
				bind:value={first_name}
				placeholder={$t('register_firstname')}
				required
				autocomplete="given-name"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
		</div>

		<div>
			<label for="last_name" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				Nachname
			</label>

			<input
				id="last_name"
				type="text"
				bind:value={last_name}
				placeholder={$t('register_lastname')}
				required
				autocomplete="family-name"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
		</div>

		<div>
			<label for="email" class="mb-1 block text-sm font-medium text-[#2A2E38]"> E-Mail </label>

			<input
				id="email"
				type="email"
				bind:value={email}
				placeholder={$t('register_email')}
				required
				autocomplete="email"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
		</div>

		<div>
			<label for="password" class="mb-1 block text-sm font-medium text-[#2A2E38]"> Passwort </label>

			<input
				id="password"
				type="password"
				bind:value={password}
				placeholder={$t('register_password')}
				required
				minlength="8"
				autocomplete="new-password"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>

			<p class="mt-1 text-xs text-[#2A2E38]/50">Mindestens 8 Zeichen.</p>
		</div>

		{#if error}
			<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
				{error}
			</p>
		{/if}

		<button
			type="submit"
			disabled={loading}
			class="rounded-lg bg-[#8FB0C4] px-4 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
		>
			{loading ? 'Wird registriert...' : $t('register_button')}
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-[#2A2E38]/60">
		Du hast bereits ein Konto?

		<a href={resolve('/auth/login')} class="font-semibold text-[#8FB0C4] hover:text-[#62AA97]">
			Login
		</a>
	</p>
</div>
