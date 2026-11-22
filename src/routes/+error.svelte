
<script>
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import * as m from '$lib/paraglide/messages.js';
</script>

<svelte:head>
	<title>{m.error_label()} {page.status} | NextJob</title>
</svelte:head>

<section class="flex min-h-[65vh] flex-col items-center justify-center px-4 text-center">
	<p class="text-sm font-medium text-gray-500">{m.error_label()}</p>

	<h1 class="mt-2 text-6xl font-bold text-gray-900 md:text-7xl">
		{page.status}
	</h1>

	<h2 class="mt-4 text-2xl font-semibold text-gray-900">{m.error_heading()}</h2>

	<p class="mt-3 max-w-md text-gray-600">
		{page.error?.message ?? m.error_description()}
	</p>

	<a
		href={resolve('/')}
		class="mt-8 rounded-lg bg-gray-900 px-5 py-3 font-medium text-white transition hover:bg-gray-700"
	>
		{m.error_back_home()}
	</a>
</section>
