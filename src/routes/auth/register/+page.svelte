<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
	import { API_URL } from '$lib/api.js';

	let first_name = $state('');
	let last_name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let role = $state('');
	let showPassword = $state(false);

	let error = $state('');
	let loading = $state(false);

	let passwordsMatch = $derived(password === confirmPassword);

	async function register(e) {
		e.preventDefault();
		error = '';

		if (!role) {
			error = 'register_role_error';
			return;
		}

		if (!passwordsMatch) {
			error = 'register_password_mismatch';
			return;
		}

		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					first_name: first_name.trim(),
					last_name: last_name.trim(),
					email: email.trim().toLowerCase(),
					password
					// role erst hinzufügen, wenn Leon
					// das API-Feld bestätigt hat.
				})
			});

			const data = await res.json();

			if (!res.ok) {
				if (data.error === 'Email already registered') {
					error = 'register_email_exists';
				} else {
					error = data.error || 'register_failed';
				}
				return;
			}

			goto(resolve('/auth/verifizierung'));
		} catch {
			error = 'common_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{$t('register_button')} | NextJob</title>
</svelte:head>

<div class="mx-auto max-w-md px-4 py-12">
	<h1 class="text-3xl font-bold text-[#2A2E38]">
		{$t('register_title')}
	</h1>

	<p class="mt-2 text-sm text-[#2A2E38]/60">
		{$t('register_description')}
	</p>

	<form onsubmit={register} class="mt-6 flex flex-col gap-4">
		<div>
			<p class="mb-2 text-sm font-medium text-[#2A2E38]">
				{$t('register_role_question')}
			</p>

			<div class="grid grid-cols-2 gap-3">
				<label
					class={`cursor-pointer rounded-xl border-2 p-4 text-center transition ${
						role === 'jobnehmer'
							? 'border-[#62AA97] bg-[#62AA97]/10'
							: 'border-[#8FB0C4]/40 bg-white'
					}`}
				>
					<input
						type="radio"
						name="role"
						value="jobnehmer"
						bind:group={role}
						required
						class="mb-2 accent-[#62AA97]"
					/>
					<span class="block font-semibold text-[#2A2E38]">
						{$t('register_worker')}
					</span>
					<span class="mt-1 block text-xs text-[#2A2E38]/60">
						{$t('register_worker_desc')}
					</span>
				</label>

				<label
					class={`cursor-pointer rounded-xl border-2 p-4 text-center transition ${
						role === 'jobgeber'
							? 'border-[#62AA97] bg-[#62AA97]/10'
							: 'border-[#8FB0C4]/40 bg-white'
					}`}
				>
					<input
						type="radio"
						name="role"
						value="jobgeber"
						bind:group={role}
						required
						class="mb-2 accent-[#62AA97]"
					/>
					<span class="block font-semibold text-[#2A2E38]">
						{$t('register_employer')}
					</span>
					<span class="mt-1 block text-xs text-[#2A2E38]/60">
						{$t('register_employer_desc')}
					</span>
				</label>
			</div>

			<p class="mt-2 text-xs text-[#2A2E38]/60">
				{$t('register_role_note')}
			</p>
		</div>

		<div>
			<label for="first_name" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				{$t('register_firstname')}
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
				{$t('register_lastname')}
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
			<label for="email" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				{$t('register_email')}
			</label>
			<input
				id="email"
				type="email"
				bind:value={email}
				placeholder={$t('register_email')}
				required
				autocomplete="email"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
			<p class="mt-1 text-xs text-[#2A2E38]/50">
				{$t('register_email_hint')}
			</p>
		</div>

		<div>
			<label for="password" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				{$t('common_password')}
			</label>
			<input
				id="password"
				type={showPassword ? 'text' : 'password'}
				bind:value={password}
				placeholder={$t('register_password')}
				required
				minlength="8"
				autocomplete="new-password"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>
			<p class="mt-1 text-xs text-[#2A2E38]/50">
				{$t('register_password_hint')}
			</p>
		</div>

		<div>
			<label for="confirmPassword" class="mb-1 block text-sm font-medium text-[#2A2E38]">
				{$t('register_confirm_password')}
			</label>
			<input
				id="confirmPassword"
				type={showPassword ? 'text' : 'password'}
				bind:value={confirmPassword}
				placeholder={$t('register_repeat_password')}
				required
				autocomplete="new-password"
				class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
			/>

			{#if confirmPassword && !passwordsMatch}
				<p class="mt-1 text-xs text-red-600">
					{$t('register_password_mismatch')}
				</p>
			{/if}
		</div>

		<label class="flex items-center gap-2 text-sm text-[#2A2E38]">
			<input
				type="checkbox"
				bind:checked={showPassword}
				class="accent-[#62AA97]"
			/>
			{$t('register_show_password')}
		</label>

		{#if error}
			<p role="alert" class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
				{['register_role_error', 'register_password_mismatch', 'register_email_exists', 'register_failed', 'common_server_error'].includes(error) ? $t(error) : error}
			</p>
		{/if}

		<button
			type="submit"
			disabled={loading || !role || !passwordsMatch}
			class="rounded-lg bg-[#8FB0C4] px-4 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
		>
			{loading ? $t('register_loading') : $t('register_button')}
		</button>
	</form>

	<p class="mt-6 text-center text-sm text-[#2A2E38]/60">
		{$t('register_have_account')}
		<a
			href={resolve('/auth/login')}
			class="font-semibold text-[#8FB0C4] hover:text-[#62AA97]"
		>
			{$t('nav_login')}
		</a>
	</p>
</div>