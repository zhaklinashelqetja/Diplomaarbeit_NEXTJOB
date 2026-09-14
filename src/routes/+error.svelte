<script>
	import { page } from '$app/state';
</script>

<svelte:head>
	<title>Fehler {page.status} | NextJob</title>
</svelte:head>

<section class="flex min-h-[65vh] flex-col items-center justify-center px-4 text-center">
	<p class="text-sm font-medium text-gray-500">
		Fehler
	</p>

	<h1 class="mt-2 text-6xl font-bold text-gray-900 md:text-7xl">
		{page.status}
	</h1>

	<h2 class="mt-4 text-2xl font-semibold text-gray-900">
		Etwas ist schiefgelaufen
	</h2>

	<p class="mt-3 max-w-md text-gray-600">
		{page.error?.message ?? 'Diese Seite existiert nicht oder ist nicht verfügbar.'}
	</p>

	<a
		href="/"
		class="mt-8 rounded-lg bg-gray-900 px-5 py-3 font-medium text-white transition hover:bg-gray-700"
	>
		Zurück zur Startseite
	</a>
</section>