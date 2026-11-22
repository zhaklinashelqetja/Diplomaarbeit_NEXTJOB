
<script>
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';
	import * as m from '$lib/paraglide/messages.js';
	import { ArrowLeft, ArrowUpRight, Mail, LockKeyhole, MapPin } from '@lucide/svelte';

	let email = $state('');
	let error = $state('');
	let success = $state('');
	let loading = $state(false);

	function translateError(key) {
		const messages = {
			common_error: m.common_error,
			common_server_error: m.common_server_error
		};

		return messages[key]?.() ?? key;
	}

	async function forgotPassword(e) {
		e.preventDefault();

		error = '';
		success = '';
		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/forgot-password`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({ email })
			});

			const data = await res.json();

			if (!res.ok) {
				error = data.error || 'common_error';
				return;
			}

			success = 'forgot_success';
			email = '';
		} catch {
			error = 'common_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{m.forgot_title()} | NextJob</title>
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
					{m.forgot_visual_eyebrow()}
				</p>

				<h2 class="max-w-md text-5xl font-semibold leading-[1.08] tracking-[-0.055em]">
					{m.forgot_visual_title1()}<br />
					{m.forgot_visual_title2()}
				</h2>

				<p class="mt-6 max-w-sm text-sm leading-7 text-white/80">
					{m.forgot_visual_description()}
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
					{m.forgot_eyebrow()}
				</p>

				<span class="text-xs tracking-[0.12em] text-[#2A2E38]/40">
					03 / NEXTJOB
				</span>
			</div>

			<div class="mb-10">
				<div class="mb-7 flex h-14 w-14 items-center justify-center rounded-2xl bg-[#62AA97]/10 text-[#5B9F8D]">
					<LockKeyhole size={26} strokeWidth={1.5} />
				</div>

				<h1 class="text-[clamp(40px,4vw,58px)] font-semibold leading-[1.05] tracking-[-0.055em]">
					{m.forgot_title()}<span class="text-[#62AA97]">.</span>
				</h1>

				<p class="mt-5 max-w-sm text-sm leading-7 text-[#2A2E38]/60">
					{m.forgot_description()}
				</p>
			</div>

			<form onsubmit={forgotPassword} class="flex flex-col gap-6">
				<div>
					<label for="email" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
						{m.common_email()}
					</label>

					<div class="relative">
						<Mail
							size={19}
							strokeWidth={1.5}
							class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#2A2E38]/40"
						/>

						<input
							id="email"
							type="email"
							bind:value={email}
							placeholder={m.forgot_email_placeholder()}
							required
							autocomplete="email"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] py-4 pl-12 pr-4 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>
				</div>

				{#if error}
					<p role="alert" class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
						{translateError(error)}
					</p>
				{/if}

				{#if success}
					<p role="status" class="rounded-xl border border-[#62AA97]/30 bg-[#62AA97]/10 px-4 py-3 text-sm text-[#2A2E38]">
						{m.forgot_success()}
					</p>
				{/if}

				<button
					type="submit"
					disabled={loading}
					class="group flex w-full items-center justify-center gap-3 rounded-xl bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
				>
					{loading ? m.forgot_loading() : m.forgot_send()}

					<ArrowUpRight
						size={19}
						strokeWidth={1.7}
						class="transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
					/>
				</button>
			</form>

			<div class="mt-10 border-t border-[#2A2E38]/10 pt-7">
				<a
					href={resolve('/auth/login')}
					class="flex items-center justify-center gap-2 text-sm font-semibold text-[#5B9F8D] transition-colors hover:text-[#2A2E38]"
				>
					<ArrowLeft size={17} strokeWidth={1.7} />
					{m.forgot_back()}
				</a>
			</div>
		</div>
	</div>
</section>
