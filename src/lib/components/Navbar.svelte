<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { locale } from '$lib/i18n.js';
	import { isLoggedIn, checkLogin, logout } from '$lib/auth.js';
	import { onMount } from 'svelte';

	let menuOpen = $state(false);

	onMount(() => {
		checkLogin();
	});

	function toggleLanguage() {
		locale.update((current) => (current === 'de' ? 'al' : 'de'));
	}

	function closeMenu() {
		menuOpen = false;
	}

	function handleLogout() {
		logout();
		menuOpen = false;
		goto(resolve('/'));
	}
</script>

<nav class="sticky top-0 z-50 border-b border-[#8FB0C4]/30 bg-[#F5F1EE]">
	<div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
		<!-- Logo -->
		<a href={resolve('/')} class="flex items-center gap-2" aria-label="NextJob Startseite">
			<img src="/images/nextjob-logo.png" alt="NextJob Logo" class="h-10 w-auto object-contain" />

			<span
				class="text-2xl font-bold tracking-wide text-[#2A2E38]"
				style="font-family: var(--font-logo);"
			>
				NEXTJOB
			</span>
		</a>

		<!-- Desktop Navigation -->
		<div class="hidden items-center gap-6 md:flex">
			<a href={resolve('/')} class="font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]">
				Start
			</a>

			<a href={resolve('/jobs')} class="font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]">
				Jobs finden
			</a>

			{#if $isLoggedIn}
				<a
					href={resolve('/chat')}
					class="font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]"
				>
					Chat
				</a>

				<a
					href={resolve('/benachrichtigungen')}
					class="font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]"
				>
					Benachrichtigungen
				</a>
			{:else}
				<a
					href={resolve('/wer-wir-sind')}
					class="font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]"
				>
					Wer wir sind
				</a>
			{/if}

			<!-- Sprache -->
			<button
				type="button"
				onclick={toggleLanguage}
				class="rounded-lg border border-[#8FB0C4] px-3 py-2 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#8FB0C4]/20"
			>
				{$locale === 'de' ? 'AL' : 'DE'}
			</button>

			{#if $isLoggedIn}
				<button
					type="button"
					onclick={handleLogout}
					class="rounded-lg bg-[#8FB0C4] px-5 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
				>
					Abmelden
				</button>
			{:else}
				<a
					href={resolve('/auth/login')}
					class="px-2 py-2 font-medium text-[#2A2E38] transition hover:text-[#8FB0C4]"
				>
					Login
				</a>

				<a
					href={resolve('/auth/register')}
					class="rounded-lg bg-[#8FB0C4] px-5 py-2.5 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
				>
					Registrieren
				</a>
			{/if}
		</div>

		<!-- Mobile -->
		<div class="flex items-center gap-3 md:hidden">
			<button
				type="button"
				onclick={toggleLanguage}
				class="rounded-lg border border-[#8FB0C4] px-3 py-1.5 text-sm font-semibold text-[#2A2E38]"
			>
				{$locale === 'de' ? 'AL' : 'DE'}
			</button>

			<button
				type="button"
				aria-label="Menü öffnen"
				aria-expanded={menuOpen}
				onclick={() => (menuOpen = !menuOpen)}
				class="flex h-10 w-10 items-center justify-center rounded-lg text-2xl text-[#2A2E38] hover:bg-[#8FB0C4]/20"
			>
				{menuOpen ? '✕' : '☰'}
			</button>
		</div>
	</div>

	<!-- Mobile Menü -->
	{#if menuOpen}
		<div class="border-t border-[#8FB0C4]/30 bg-[#F5F1EE] px-4 py-4 md:hidden">
			<div class="mx-auto flex max-w-6xl flex-col gap-1">
				<a
					href={resolve('/')}
					onclick={closeMenu}
					class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
				>
					Start
				</a>

				<a
					href={resolve('/jobs')}
					onclick={closeMenu}
					class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
				>
					Jobs finden
				</a>

				{#if $isLoggedIn}
					<a
						href={resolve('/chat')}
						onclick={closeMenu}
						class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
					>
						Chat
					</a>

					<a
						href={resolve('/benachrichtigungen')}
						onclick={closeMenu}
						class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
					>
						Benachrichtigungen
					</a>

					<button
						type="button"
						onclick={handleLogout}
						class="mt-2 rounded-lg bg-[#8FB0C4] px-4 py-3 text-left font-semibold text-[#2A2E38] hover:bg-[#62AA97]"
					>
						Abmelden
					</button>
				{:else}
					<a
						href={resolve('/wer-wir-sind')}
						onclick={closeMenu}
						class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
					>
						Wer wir sind
					</a>

					<a
						href={resolve('/auth/login')}
						onclick={closeMenu}
						class="rounded-lg px-3 py-3 font-medium text-[#2A2E38] hover:bg-[#8FB0C4]/15"
					>
						Login
					</a>

					<a
						href={resolve('/auth/register')}
						onclick={closeMenu}
						class="mt-2 rounded-lg bg-[#8FB0C4] px-4 py-3 text-center font-semibold text-[#2A2E38] hover:bg-[#62AA97]"
					>
						Registrieren
					</a>
				{/if}
			</div>
		</div>
	{/if}
</nav>
