
<script>
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
	import { API_URL } from '$lib/api.js';

	let loading = $state(false);
	let success = $state(false);
	let error = $state('');

	async function resendVerification() {
		error = '';
		success = false;

		const token = localStorage.getItem('token');

		if (!token) {
			error = 'verify_login_required';
			return;
		}

		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/verify/request`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				error = 'verify_resend_failed';
				return;
			}

			success = true;
		} catch {
			error = 'common_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{$t('verify_title')} | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<div class="text-5xl">✉️</div>

		<h1 class="mt-5 text-3xl font-bold text-[#2A2E38]">
			{$t('verify_title')}
		</h1>

		<p class="mt-4 text-[#2A2E38]/70">
			{$t('verify_description')}
		</p>

		<p class="mt-4 text-sm text-[#2A2E38]/50">
			{$t('verify_spam')}
		</p>

		{#if success}
			<p
				role="status"
				class="mt-5 rounded-lg bg-[#62AA97]/10 px-3 py-3 text-sm text-[#2A2E38]"
			>
				{$t('verify_resend_success')}
			</p>
		{/if}

		{#if error}
			<p
				role="alert"
				class="mt-5 rounded-lg bg-red-50 px-3 py-3 text-sm text-red-600"
			>
				{$t(error)}
			</p>
		{/if}

		<button
			type="button"
			onclick={resendVerification}
			disabled={loading}
			class="mt-6 w-full rounded-lg border border-[#8FB0C4] px-5 py-3 font-semibold text-[#2A2E38] transition hover:bg-[#8FB0C4]/10 disabled:cursor-not-allowed disabled:opacity-60"
		>
			{loading ? $t('verify_resending') : $t('verify_resend')}
		</button>

		<a
			href={resolve('/auth/login')}
			class="mt-4 inline-block rounded-lg bg-[#8FB0C4] px-5 py-3 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
		>
			{$t('verify_login')}
		</a>
	</div>
</section>
