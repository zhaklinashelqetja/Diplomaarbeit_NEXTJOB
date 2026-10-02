<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
	import { API_URL } from '$lib/api.js';
	import { isLoggedIn } from '$lib/auth.js';

	let email = $state('');
	let password = $state('');
	let error = $state('');
	let loading = $state(false);

	async function login(e) {
		e.preventDefault();

		error = '';
		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/login`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					email,
					password
				})
			});

			const data = await res.json();

			if (!res.ok) {
				if (data.error === 'Wrong email or password') {
					error = 'E-Mail-Adresse oder Passwort ist falsch.';
				} else if (data.error === 'Email not verified') {
					error = 'Bitte bestätige zuerst deine E-Mail-Adresse.';
				} else {
					error = data.error || 'Login fehlgeschlagen.';
				}

				return;
			}

			localStorage.setItem('token', data.token);
			isLoggedIn.set(true);

			goto(resolve('/'));
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>Login | NextJob</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-3xl font-bold text-[#2A2E38]">
		{$t('login_title')}
	</h1>

	<p class="mt-2 text-sm text-[#2A2E38]/60">Melde dich bei deinem NextJob-Konto an.</p>

	<form onsubmit={login} class="mt-6 flex flex-col gap-4">
		<div>
			<label for="email" class="mb-1 block text-sm font-medium text-[#2A2E38]"> E-Mail </label>

			<input
				id="email"
				type="email"
				bind:value={email}
				placeholder={$t('login_email')}
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
				placeholder={$t('login_password')}
				required
				minlength="8"
				autocomplete="current-password"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
		</div>

		<div class="text-right">
			<a
				href={resolve('/auth/passwort-vergessen')}
				class="text-sm font-medium text-[#8FB0C4] hover:text-[#62AA97]"
			>
				Passwort vergessen?
			</a>
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
			{loading ? 'Anmelden...' : $t('login_button')}
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-[#2A2E38]/60">
		Noch kein Konto?

		<a href={resolve('/auth/register')} class="font-semibold text-[#8FB0C4] hover:text-[#62AA97]">
			Registrieren
		</a>
	</p>
</div>
