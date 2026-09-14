<script>
	import { resolve } from '$app/paths';
	import { locale } from '$lib/i18n.js';

	let menuOpen = $state(false);

	function toggleLanguage() {
		locale.update((current) => (current === 'de' ? 'al' : 'de'));
	}

	function closeMenu() {
		menuOpen = false;
	}
</script>

<nav class="sticky top-0 z-50 border-b border-gray-200 bg-white">
	<div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
		<a href={resolve('/')} class="text-xl font-bold text-gray-900"> NextJob </a>

		<div class="hidden items-center gap-6 md:flex">
			<a href={resolve('/')} class="text-gray-700 transition hover:text-gray-900"> Start </a>

			<a href={resolve('/wer-wir-sind')} class="text-gray-700 transition hover:text-gray-900">
				Wer wir sind
			</a>

			<button
				type="button"
				onclick={toggleLanguage}
				class="rounded-md border border-gray-300 px-3 py-2 text-sm font-medium text-gray-700 hover:bg-gray-100"
			>
				{$locale === 'de' ? 'AL' : 'DE'}
			</button>

			<a
				href={resolve('/auth/login')}
				class="rounded-lg bg-gray-900 px-4 py-2 text-white transition hover:bg-gray-700"
			>
				Login
			</a>
		</div>

		<div class="flex items-center gap-3 md:hidden">
			<button
				type="button"
				onclick={toggleLanguage}
				class="rounded-md border border-gray-300 px-2 py-1 text-sm"
			>
				{$locale === 'de' ? 'AL' : 'DE'}
			</button>

			<button
				type="button"
				aria-label="Menü öffnen"
				aria-expanded={menuOpen}
				onclick={() => (menuOpen = !menuOpen)}
				class="text-2xl text-gray-900"
			>
				{menuOpen ? '✕' : '☰'}
			</button>
		</div>
	</div>

	{#if menuOpen}
		<div class="border-t border-gray-200 bg-white px-4 py-4 md:hidden">
			<div class="mx-auto flex max-w-6xl flex-col gap-4">
				<a href={resolve('/')} onclick={closeMenu} class="text-gray-700"> Start </a>

				<a href={resolve('/wer-wir-sind')} onclick={closeMenu} class="text-gray-700">
					Wer wir sind
				</a>

				<a
					href={resolve('/auth/login')}
					onclick={closeMenu}
					class="rounded-lg bg-gray-900 px-4 py-2 text-center text-white"
				>
					Login
				</a>
			</div>
		</div>
	{/if}
</nav>
