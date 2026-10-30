<script>
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
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

		<a
			href={resolve('/auth/login')}
			class="mt-8 inline-block rounded-lg bg-[#8FB0C4] px-5 py-3 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
		>
			{$t('verify_login')}
		</a>
	</div>
</section>