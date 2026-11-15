
<script>
	import '../app.css';
	import Navbar from '$lib/components/Navbar.svelte';
	import Footer from '$lib/components/Footer.svelte';
	import { onMount } from 'svelte';
	import { checkLogin } from '$lib/auth.js';

	let { children } = $props();

	onMount(() => {
		// Login-Status und Benutzerdaten laden
		checkLogin();

		// PWA Service Worker registrieren
		async function registerServiceWorker() {
			if ('serviceWorker' in navigator) {
				const { registerSW } = await import('virtual:pwa-register');
				registerSW({ immediate: true });
			}
		}

		registerServiceWorker();
	});
</script>

<div class="flex min-h-screen flex-col">
	<Navbar />

	<main class="flex-1">
		{@render children()}
	</main>

	<Footer />
</div>
