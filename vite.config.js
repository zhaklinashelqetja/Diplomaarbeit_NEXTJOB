
import { paraglideVitePlugin } from '@inlang/paraglide-js';
import { sveltekit } from '@sveltejs/kit/vite';
import { SvelteKitPWA } from '@vite-pwa/sveltekit';
import tailwindcss from '@tailwindcss/vite';
import { defineConfig } from 'vite';

export default defineConfig({
    plugins: [
        paraglideVitePlugin({
            project: './project.inlang',
            outdir: './src/lib/paraglide',
            emitTsDeclarations: true
        }),

        tailwindcss(),

        sveltekit(),

        SvelteKitPWA({
            registerType: 'autoUpdate',

            devOptions: {
                enabled: true
            },

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
                        src: '/images/nextjob-icon-192.png',
                        sizes: '192x192',
                        type: 'image/png'
                    },
                    {
                        src: '/images/nextjob-icon-512.png',
                        sizes: '512x512',
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
