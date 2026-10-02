import { sveltekit } from '@sveltejs/kit/vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [
		tailwindcss(),
		sveltekit(),

		SvelteKitPWA({
			registerType: 'autoUpdate',

			manifest: {
				name: 'NextJob',
				short_name: 'NextJob',
				description: 'Digitale Jobvermittlung für lokale Dienstleistungen in Shkodër',

				theme_color: '#8FB0C4',
				background_color: '#F5F1EE',

				display: 'standalone',
				start_url: '/',
				lang: 'de',

				icons: [
					{
						src: '/images/nextjob-logo.png',
						type: 'image/png'
					}
				]
			},

			workbox: {
				globPatterns: ['**/*.{js,css,html,png,svg,ico}']
			}
		})
	]
});