
<script>
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';
	import * as m from '$lib/paraglide/messages.js';

	let password = $state('');
	let confirmPassword = $state('');
	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	function translateError(key) {
		const messages = {
			reset_password_mismatch: m.reset_password_mismatch,
			reset_password_too_short: m.reset_password_too_short,
			reset_password_invalid_link: m.reset_password_invalid_link,
			reset_password_failed: m.reset_password_failed,
			reset_password_server_error: m.reset_password_server_error
		};

		return messages[key]?.() ?? key;
	}

	async function resetPassword(e) {
		e.preventDefault();

		error = '';
		success = '';

		if (password !== confirmPassword) {
			error = 'reset_password_mismatch';
			return;
		}

		if (password.length < 8) {
			error = 'reset_password_too_short';
			return;
		}

		const token = page.url.searchParams.get('token');

		if (!token) {
			error = 'reset_password_invalid_link';
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
				error = data.error || 'reset_password_failed';
				return;
			}

			success = 'reset_password_success';
			password = '';
			confirmPassword = '';
		} catch {
			error = 'reset_password_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{m.reset_password_page_title()} | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<h1 class="text-3xl font-bold text-[#2A2E38]">{m.reset_password_title()}</h1>

		<p class="mt-2 text-sm text-[#2A2E38]/60">
			{m.reset_password_description()}
		</p>

		<form onsubmit={resetPassword} class="mt-6 flex flex-col gap-4">
			<div>
				<label for="password" class="mb-1 block text-sm font-medium text-[#2A2E38]">
					{m.reset_password_new()}
				</label>

				<input
					id="password"
					type="password"
					bind:value={password}
					placeholder={m.reset_password_new()}
					required
					minlength="8"
					autocomplete="new-password"
					class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
				/>

				<p class="mt-1 text-xs text-[#2A2E38]/50">{m.reset_password_hint()}</p>
			</div>

			<div>
				<label for="confirmPassword" class="mb-1 block text-sm font-medium text-[#2A2E38]">
					{m.reset_password_confirm()}
				</label>

				<input
					id="confirmPassword"
					type="password"
					bind:value={confirmPassword}
					placeholder={m.reset_password_confirm()}
					required
					minlength="8"
					autocomplete="new-password"
					class="w-full rounded-lg border border-[#8FB0C4]/50 bg-white px-3 py-2.5 text-[#2A2E38] outline-none focus:border-[#8FB0C4]"
				/>
			</div>

			{#if error}
				<p class="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-600">
					{translateError(error)}
				</p>
			{/if}

			{#if success}
				<div class="rounded-lg bg-[#62AA97]/10 px-3 py-3">
					<p class="text-sm text-[#2A2E38]">
						{m.reset_password_success()}
					</p>

					<a
						href={resolve('/auth/login')}
						class="mt-2 inline-block text-sm font-semibold text-[#62AA97] hover:underline"
					>
						{m.reset_password_login()}
					</a>
				</div>
			{/if}

			<button
				type="submit"
				disabled={loading || success}
				class="rounded-lg bg-[#8FB0C4] px-4 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
			>
				{loading ? m.reset_password_loading() : m.reset_password_button()}
			</button>
		</form>
	</div>
</section>
