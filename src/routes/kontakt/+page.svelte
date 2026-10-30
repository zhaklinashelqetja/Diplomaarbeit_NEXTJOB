<script>
	import { t } from '$lib/i18n.js';
</script>

<svelte:head>
	<title>{$t('contact_title')} | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-4xl px-4 py-16">
	<h1 class="text-4xl font-bold text-gray-900">
		{$t('contact_title')}
	</h1>

	<p class="mt-4 max-w-2xl text-gray-600">
		{$t('contact_description')}
	</p>

	<div class="mt-8 rounded-xl border border-gray-200 bg-white p-6">
		<h2 class="text-xl font-semibold text-gray-900">NextJob</h2>

		<p class="mt-4 text-gray-600">
			{$t('contact_location')}
		</p>

		<p class="mt-2 text-gray-600">
			{$t('contact_email')}: nextjob@example.com
		</p>
	</div>
</section>