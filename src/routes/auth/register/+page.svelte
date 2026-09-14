<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';

	let first_name = $state('');
	let last_name = $state('');
	let email = $state('');
	let password = $state('');
	let error = $state('');

	async function register(e) {
		e.preventDefault();
		error = '';

		const res = await fetch('http://localhost:5000/api/auth/register', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ first_name, last_name, email, password })
		});

		const data = await res.json();

		if (!res.ok) {
			error = data.error;
			return;
		}

		localStorage.setItem('token', data.token);

		goto(resolve('/'));
	}
</script>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-2xl font-bold">
		{$t('register_title')}
	</h1>

	<form onsubmit={register} class="mt-6 flex flex-col gap-4">
		<input
			type="text"
			bind:value={first_name}
			placeholder={$t('register_firstname')}
			class="rounded-lg border px-3 py-2"
		/>

		<input
			type="text"
			bind:value={last_name}
			placeholder={$t('register_lastname')}
			class="rounded-lg border px-3 py-2"
		/>

		<input
			type="email"
			bind:value={email}
			placeholder={$t('register_email')}
			class="rounded-lg border px-3 py-2"
		/>

		<input
			type="password"
			bind:value={password}
			placeholder={$t('register_password')}
			class="rounded-lg border px-3 py-2"
		/>

		{#if error}
			<p class="text-sm text-red-600">
				{error}
			</p>
		{/if}

		<button type="submit" class="rounded-lg bg-gray-900 px-4 py-2 text-white">
			{$t('register_button')}
		</button>
	</form>
</div>
