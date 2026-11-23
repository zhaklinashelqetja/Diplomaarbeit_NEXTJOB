
<script>
	import { resolve } from '$app/paths';
	import * as m from '$lib/paraglide/messages.js';
	import { API_URL } from '$lib/api.js';
	import { isLoggedIn, currentUser } from '$lib/auth.js';
	import {
		ArrowLeft,
		ArrowUpRight,
		Mail,
		MailCheck,
		MailWarning,
		MapPin,
		RefreshCw
	} from '@lucide/svelte';

	let loading = $state(false);
	let success = $state(false);
	let error = $state('');

	let alreadyVerified = $derived(
		$isLoggedIn && $currentUser?.is_verified === true
	);

	function translateError(key) {
		const messages = {
			verify_login_required: m.verify_login_required,
			verify_resend_wait: m.verify_resend_wait,
			verify_already_verified: m.verify_already_verified,
			verify_resend_failed: m.verify_resend_failed,
			common_server_error: m.common_server_error
		};

		return messages[key]?.() ?? key;
	}

	async function resendVerification() {
		if (loading || alreadyVerified) return;

		error = '';
		success = false;

		const token = localStorage.getItem('token');

		if (!token) {
			error = 'verify_login_required';
			return;
		}

		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/verify/request`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				}
			});

			if (!res.ok) {
				if (res.status === 429) {
					error = 'verify_resend_wait';
				} else if (res.status === 401) {
					error = 'verify_login_required';
				} else if (res.status === 400) {
					error = 'verify_already_verified';
				} else {
					error = 'verify_resend_failed';
				}
				return;
			}

			success = true;
		} catch {
			error = 'common_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{m.verify_title()} | NextJob</title>
</svelte:head>

<section class="relative overflow-hidden bg-[#F5F1EE] px-5 py-16 text-[#2A2E38] sm:px-8 sm:py-20 lg:py-24">
	<div
		class="pointer-events-none absolute -right-28 -top-32 h-96 w-96 rounded-full bg-[#8FB0C4]/15 blur-3xl"
	></div>

	<div
		class="pointer-events-none absolute -bottom-40 -left-32 h-96 w-96 rounded-full bg-[#62AA97]/15 blur-3xl"
	></div>

	<div
		class="relative mx-auto grid max-w-6xl overflow-hidden rounded-[30px] border border-[#2A2E38]/10 bg-white/75 shadow-[0_25px_80px_-45px_rgba(42,46,56,0.35)] backdrop-blur-sm lg:grid-cols-[0.95fr_1.05fr]"
	>
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
					{m.verify_visual_eyebrow()}
				</p>

				<h2 class="max-w-md text-5xl font-semibold leading-[1.08] tracking-[-0.055em]">
					{m.verify_visual_title1()}<br />
					{m.verify_visual_title2()}
				</h2>

				<p class="mt-6 max-w-sm text-sm leading-7 text-white/80">
					{m.verify_visual_description()}
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
					{m.verify_eyebrow()}
				</p>

				<span class="text-xs tracking-[0.12em] text-[#2A2E38]/40">
					04 / NEXTJOB
				</span>
			</div>

			<div class="mb-9">
				<div
					class="mb-7 flex h-16 w-16 items-center justify-center rounded-2xl bg-[#62AA97]/10 text-[#5B9F8D]"
				>
					{#if alreadyVerified}
						<MailCheck size={30} strokeWidth={1.5} />
					{:else}
						<Mail size={30} strokeWidth={1.5} />
					{/if}
				</div>

				<h1 class="text-[clamp(40px,4vw,58px)] font-semibold leading-[1.05] tracking-[-0.055em]">
					{m.verify_title()}<span class="text-[#62AA97]">.</span>
				</h1>

				{#if alreadyVerified}
					<p class="mt-5 max-w-sm text-sm leading-7 text-[#2A2E38]/60">
						{m.verify_already_verified_description()}
					</p>
				{:else}
					<p class="mt-5 max-w-sm text-sm leading-7 text-[#2A2E38]/60">
						{m.verify_description()}
					</p>
				{/if}
			</div>

			{#if alreadyVerified}
				<div class="mb-7 flex items-start gap-3 rounded-xl border border-[#62AA97]/30 bg-[#62AA97]/10 px-4 py-4">
					<MailCheck size={22} strokeWidth={1.5} class="mt-0.5 shrink-0 text-[#5B9F8D]" />

					<p class="text-sm leading-6 text-[#2A2E38]">
						{m.verify_already_verified()}
					</p>
				</div>
			{:else}
				<div class="mb-7 flex items-start gap-3 rounded-xl border border-[#8FB0C4]/30 bg-[#F9F8F6] px-4 py-4">
					<MailWarning size={21} strokeWidth={1.5} class="mt-0.5 shrink-0 text-[#5B9F8D]" />

					<p class="text-sm leading-6 text-[#2A2E38]/65">
						{m.verify_spam()}
					</p>
				</div>

				{#if success}
					<p
						role="status"
						class="mb-5 rounded-xl border border-[#62AA97]/30 bg-[#62AA97]/10 px-4 py-3 text-sm leading-6 text-[#2A2E38]"
					>
						{m.verify_resend_success()}
					</p>
				{/if}

				{#if error}
					<p
						role="alert"
						class="mb-5 rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm leading-6 text-red-600"
					>
						{translateError(error)}
					</p>
				{/if}

				<button
					type="button"
					onclick={resendVerification}
					disabled={loading}
					class="group flex w-full items-center justify-center gap-3 rounded-xl border border-[#8FB0C4]/50 bg-[#F9F8F6] px-6 py-4 text-sm font-semibold text-[#2A2E38] transition-all duration-200 hover:border-[#62AA97] hover:bg-[#62AA97]/10 disabled:cursor-not-allowed disabled:opacity-60"
				>
					<RefreshCw size={18} strokeWidth={1.7} class={loading ? 'animate-spin' : ''} />

					{loading ? m.verify_resending() : m.verify_resend()}
				</button>
			{/if}

			<a
				href={resolve($isLoggedIn ? '/' : '/auth/login')}
				class="group mt-4 flex w-full items-center justify-center gap-3 rounded-xl bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#62AA97]"
			>
				{#if $isLoggedIn}
					{m.nav_start()}
				{:else}
					{m.verify_login()}
				{/if}

				<ArrowUpRight
					size={19}
					strokeWidth={1.7}
					class="transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
				/>
			</a>

			<div class="mt-10 border-t border-[#2A2E38]/10 pt-7">
				<a
					href={resolve('/')}
					class="flex items-center justify-center gap-2 text-sm font-semibold text-[#5B9F8D] transition-colors hover:text-[#2A2E38]"
				>
					<ArrowLeft size={17} strokeWidth={1.7} />
					{m.verify_back_home()}
				</a>
			</div>
		</div>
	</div>
</section>
