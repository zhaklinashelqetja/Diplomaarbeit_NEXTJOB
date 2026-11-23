
<script>
	import { onMount } from 'svelte';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';
	import { loadCurrentUser } from '$lib/auth.js';
	import * as m from '$lib/paraglide/messages.js';
	import { ArrowLeft, ArrowUpRight, MailCheck, Mail, MapPin, LoaderCircle } from '@lucide/svelte';

	let loading = $state(true);
	let success = $state(false);
	let message = $state('');

	function translateMessage(key) {
		const messages = {
			verify_email_invalid_link: m.verify_email_invalid_link,
			verify_email_failed: m.verify_email_failed,
			verify_email_success: m.verify_email_success,
			verify_email_server_error: m.verify_email_server_error
		};

		return messages[key]?.() ?? key;
	}

	onMount(() => {
		let cancelled = false;

		async function verifyEmail() {
			const token = page.url.searchParams.get('token');

			if (!token) {
				message = 'verify_email_invalid_link';
				loading = false;
				return;
			}

			try {
				const res = await fetch(`${API_URL}/api/auth/verify`, {
					method: 'POST',
					headers: {
						'Content-Type': 'application/json'
					},
					body: JSON.stringify({ token })
				});

				const data = await res.json();

				if (cancelled) return;

				if (!res.ok) {
					message = data.error || 'verify_email_failed';
					return;
				}

				// Benutzerstatus nach erfolgreicher Verifizierung aktualisieren
				if (localStorage.getItem('token')) {
					await loadCurrentUser();
				}

				if (cancelled) return;

				success = true;
				message = 'verify_email_success';
			} catch {
				if (!cancelled) {
					message = 'verify_email_server_error';
				}
			} finally {
				if (!cancelled) {
					loading = false;
				}
			}
		}

		verifyEmail();

		return () => {
			cancelled = true;
		};
	});
</script>

<svelte:head>
	<title>{m.verify_email_page_title()} | NextJob</title>
</svelte:head>

<section class="relative overflow-hidden bg-[#F5F1EE] px-5 py-16 text-[#2A2E38] sm:px-8 sm:py-20 lg:py-24">
	<div class="pointer-events-none absolute -right-28 -top-32 h-96 w-96 rounded-full bg-[#8FB0C4]/15 blur-3xl"></div>
	<div class="pointer-events-none absolute -bottom-40 -left-32 h-96 w-96 rounded-full bg-[#62AA97]/15 blur-3xl"></div>

	<div class="relative mx-auto grid max-w-6xl overflow-hidden rounded-[30px] border border-[#2A2E38]/10 bg-white/75 shadow-[0_25px_80px_-45px_rgba(42,46,56,0.35)] backdrop-blur-sm lg:grid-cols-[0.95fr_1.05fr]">

		<!-- Linke Seite -->
		<div class="relative hidden min-h-[650px] overflow-hidden bg-[#2A2E38] lg:block">
			<img
				src="/images/creative-work.jpg"
				alt={m.home_image_camera()}
				class="absolute inset-0 h-full w-full object-cover"
			/>

			<div class="absolute inset-0 bg-gradient-to-t from-[#1E252C]/95 via-[#1E252C]/35 to-[#1E252C]/10"></div>

			<div class="absolute inset-x-10 top-10 flex items-center justify-between text-white">
				<span class="text-xs font-semibold uppercase tracking-[0.22em]">
					NEXTJOB
				</span>
				<MapPin size={20} strokeWidth={1.5} />
			</div>

			<div class="absolute inset-x-10 bottom-12 text-white">
				<p class="mb-5 text-xs font-semibold uppercase tracking-[0.2em] text-[#C6E3D9]">
					{m.verify_email_visual_eyebrow()}
				</p>

				<h2 class="max-w-md text-5xl font-semibold leading-[1.08] tracking-[-0.055em]">
					{m.verify_email_visual_title1()}<br />
					{m.verify_email_visual_title2()}
				</h2>

				<p class="mt-6 max-w-sm text-sm leading-7 text-white/80">
					{m.verify_email_visual_description()}
				</p>

				<div class="mt-10 flex items-center justify-between border-t border-white/25 pt-5">
					<span class="text-xs uppercase tracking-[0.15em]">
						Shkodër, Shqipëri
					</span>
					<ArrowUpRight size={24} strokeWidth={1.5} />
				</div>
			</div>
		</div>

		<!-- Rechte Seite -->
		<div class="flex flex-col justify-center px-7 py-12 sm:px-12 sm:py-16 lg:px-16">
			<div class="mb-12 flex items-center justify-between">
				<p class="text-xs font-semibold uppercase tracking-[0.2em] text-[#62AA97]">
					{m.verify_email_eyebrow()}
				</p>

				<span class="text-xs tracking-[0.12em] text-[#2A2E38]/40">
					06 / NEXTJOB
				</span>
			</div>

			<div class="mb-10">
				<div class="mb-7 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#62AA97]/10 text-[#5B9F8D]">
					{#if loading}
						<LoaderCircle size={29} strokeWidth={1.5} class="animate-spin" />
					{:else if success}
						<MailCheck size={29} strokeWidth={1.5} />
					{:else}
						<Mail size={29} strokeWidth={1.5} />
					{/if}
				</div>

				<h1 class="text-[clamp(40px,4vw,58px)] font-semibold leading-[1.05] tracking-[-0.055em]">
					{m.verify_email_title()}<span class="text-[#62AA97]">.</span>
				</h1>
			</div>

			{#if loading}
				<div class="rounded-xl border border-[#8FB0C4]/30 bg-[#F9F8F6] px-5 py-5">
					<div class="flex items-center gap-3">
						<LoaderCircle size={20} class="shrink-0 animate-spin text-[#5B9F8D]" />

						<p role="status" class="text-sm leading-6 text-[#2A2E38]/70">
							{m.verify_email_loading()}
						</p>
					</div>
				</div>
			{:else if success}
				<div class="rounded-xl border border-[#62AA97]/30 bg-[#62AA97]/10 px-5 py-5">
					<div class="mb-3 flex h-10 w-10 items-center justify-center rounded-full bg-[#62AA97] text-xl text-white">
						✓
					</div>

					<p role="status" class="text-sm leading-7 text-[#2A2E38]">
						{translateMessage(message)}
					</p>
				</div>

				<a
					href={resolve('/auth/login')}
					class="group mt-7 flex w-full items-center justify-center gap-3 rounded-xl bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#62AA97]"
				>
					{m.verify_email_login()}

					<ArrowUpRight
						size={19}
						strokeWidth={1.7}
						class="transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
					/>
				</a>
			{:else}
				<div class="rounded-xl border border-red-200 bg-red-50 px-5 py-5">
					<p role="alert" class="text-sm leading-7 text-red-600">
						{translateMessage(message)}
					</p>
				</div>

				<a
					href={resolve('/auth/verifizierung')}
					class="mt-7 flex w-full items-center justify-center gap-3 rounded-xl bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#62AA97]"
				>
					<ArrowLeft size={18} strokeWidth={1.7} />
					{m.verify_email_back()}
				</a>
			{/if}
		</div>
	</div>
</section>
