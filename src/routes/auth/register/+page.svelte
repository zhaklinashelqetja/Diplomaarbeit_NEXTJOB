
<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import * as m from '$lib/paraglide/messages.js';
	import { API_URL } from '$lib/api.js';
	import { isLoggedIn, loadCurrentUser } from '$lib/auth.js';
	import { ArrowRight, ArrowUpRight, BriefcaseBusiness, UserRound, Mail, LockKeyhole, MapPin } from '@lucide/svelte';

	let first_name = $state('');
	let last_name = $state('');
	let email = $state('');
	let password = $state('');
	let confirmPassword = $state('');
	let role = $state('');
	let showPassword = $state(false);

	let error = $state('');
	let loading = $state(false);

	let passwordsMatch = $derived(password === confirmPassword);

	function translateError(key) {
		const messages = {
			register_role_error: m.register_role_error,
			register_password_mismatch: m.register_password_mismatch,
			register_email_exists: m.register_email_exists,
			register_failed: m.register_failed,
			common_server_error: m.common_server_error
		};

		return messages[key]?.() ?? key;
	}

	async function register(e) {
		e.preventDefault();
		error = '';

		if (!role) {
			error = 'register_role_error';
			return;
		}

		if (!passwordsMatch) {
			error = 'register_password_mismatch';
			return;
		}

		loading = true;

		try {
			const res = await fetch(`${API_URL}/api/auth/register`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					first_name: first_name.trim(),
					last_name: last_name.trim(),
					email: email.trim().toLowerCase(),
					password,
					account_type: role
				})
			});

			const data = await res.json();

			if (!res.ok) {
				if (data.error === 'Email already registered') {
					error = 'register_email_exists';
				} else {
					error = data.error || 'register_failed';
				}
				return;
			}

			if (!data.token) {
				error = 'register_failed';
				return;
			}

			// Token nach erfolgreicher Registrierung speichern
			localStorage.setItem('token', data.token);
			isLoggedIn.set(true);

			// Benutzerdaten und Verifizierungsstatus laden
			await loadCurrentUser();

			// Nach der Registrierung zur passenden Hauptseite weiterleiten
			if (role === 'jobnehmer') {
				await goto(resolve('/jobnehmer/hauptseite'));
			} else if (role === 'jobgeber') {
				await goto(resolve('/jobgeber/hauptseite'));
			}
		} catch {
			error = 'common_server_error';
		} finally {
			loading = false;
		}
	}
</script>

<svelte:head>
	<title>{m.register_button()} | NextJob</title>
</svelte:head>

<section class="relative overflow-hidden bg-[#F5F1EE] px-5 py-12 text-[#2A2E38] sm:px-8 sm:py-16 lg:py-20">
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
		<div class="relative hidden min-h-[850px] overflow-hidden bg-[#2A2E38] lg:block">
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
					{m.register_visual_eyebrow()}
				</p>

				<h2 class="max-w-md text-5xl font-semibold leading-[1.08] tracking-[-0.055em]">
					{m.register_visual_title1()}<br />
					{m.register_visual_title2()}
				</h2>

				<p class="mt-6 max-w-sm text-sm leading-7 text-white/80">
					{m.register_visual_description()}
				</p>

				<div class="mt-10 flex items-center justify-between border-t border-white/25 pt-5">
					<span class="text-xs uppercase tracking-[0.15em]">
						Shkodër, Shqipëri
					</span>

					<ArrowUpRight size={24} strokeWidth={1.5} />
				</div>
			</div>
		</div>

		<!-- Rechte Seite: Registrierung -->
		<div class="flex flex-col justify-center px-7 py-12 sm:px-12 sm:py-16 lg:px-14">
			<div class="mb-10 flex items-center justify-between">
				<p class="text-xs font-semibold uppercase tracking-[0.2em] text-[#62AA97]">
					{m.register_eyebrow()}
				</p>

				<span class="text-xs tracking-[0.12em] text-[#2A2E38]/40">
					02 / NEXTJOB
				</span>
			</div>

			<div class="mb-9">
				<h1 class="text-[clamp(40px,4vw,58px)] font-semibold leading-[1.05] tracking-[-0.055em]">
					{m.register_title()}<span class="text-[#62AA97]">.</span>
				</h1>

				<p class="mt-4 max-w-sm text-sm leading-7 text-[#2A2E38]/60">
					{m.register_description()}
				</p>
			</div>

			<form onsubmit={register} class="flex flex-col gap-5">
				<div>
					<p class="mb-3 text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
						{m.register_role_question()}
					</p>

					<div class="grid grid-cols-2 gap-3">
						<label
							class={`flex cursor-pointer flex-col rounded-2xl border-2 p-4 transition-all duration-200 ${
								role === 'jobnehmer'
									? 'border-[#62AA97] bg-[#62AA97]/10'
									: 'border-[#8FB0C4]/30 bg-[#F9F8F6] hover:border-[#62AA97]/60'
							}`}
						>
							<input
								type="radio"
								name="role"
								value="jobnehmer"
								bind:group={role}
								required
								class="mb-3 accent-[#62AA97]"
							/>

							<UserRound size={23} strokeWidth={1.5} class="mb-3 text-[#5B9F8D]" />

							<span class="block text-sm font-semibold text-[#2A2E38]">
								{m.register_worker()}
							</span>

							<span class="mt-1 block text-xs leading-5 text-[#2A2E38]/60">
								{m.register_worker_desc()}
							</span>
						</label>

						<label
							class={`flex cursor-pointer flex-col rounded-2xl border-2 p-4 transition-all duration-200 ${
								role === 'jobgeber'
									? 'border-[#62AA97] bg-[#62AA97]/10'
									: 'border-[#8FB0C4]/30 bg-[#F9F8F6] hover:border-[#62AA97]/60'
							}`}
						>
							<input
								type="radio"
								name="role"
								value="jobgeber"
								bind:group={role}
								required
								class="mb-3 accent-[#62AA97]"
							/>

							<BriefcaseBusiness size={23} strokeWidth={1.5} class="mb-3 text-[#5B9F8D]" />

							<span class="block text-sm font-semibold text-[#2A2E38]">
								{m.register_employer()}
							</span>

							<span class="mt-1 block text-xs leading-5 text-[#2A2E38]/60">
								{m.register_employer_desc()}
							</span>
						</label>
					</div>
				</div>

				<div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
					<div>
						<label for="first_name" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
							{m.register_firstname()}
						</label>

						<input
							id="first_name"
							type="text"
							bind:value={first_name}
							placeholder={m.register_firstname()}
							required
							autocomplete="given-name"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] px-4 py-3.5 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>

					<div>
						<label for="last_name" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
							{m.register_lastname()}
						</label>

						<input
							id="last_name"
							type="text"
							bind:value={last_name}
							placeholder={m.register_lastname()}
							required
							autocomplete="family-name"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] px-4 py-3.5 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>
				</div>

				<div>
					<label for="email" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
						{m.register_email()}
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
							placeholder={m.register_email()}
							required
							autocomplete="email"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] py-3.5 pl-12 pr-4 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>

					<p class="mt-2 text-xs leading-5 text-[#2A2E38]/50">
						{m.register_email_hint()}
					</p>
				</div>

				<div>
					<label for="password" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
						{m.common_password()}
					</label>

					<div class="relative">
						<LockKeyhole
							size={19}
							strokeWidth={1.5}
							class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#2A2E38]/40"
						/>

						<input
							id="password"
							type={showPassword ? 'text' : 'password'}
							bind:value={password}
							placeholder={m.register_password()}
							required
							minlength="8"
							autocomplete="new-password"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] py-3.5 pl-12 pr-4 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>

					<p class="mt-2 text-xs text-[#2A2E38]/50">
						{m.register_password_hint()}
					</p>
				</div>

				<div>
					<label for="confirmPassword" class="mb-2 block text-xs font-semibold uppercase tracking-[0.12em] text-[#2A2E38]/75">
						{m.register_confirm_password()}
					</label>

					<div class="relative">
						<LockKeyhole
							size={19}
							strokeWidth={1.5}
							class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#2A2E38]/40"
						/>

						<input
							id="confirmPassword"
							type={showPassword ? 'text' : 'password'}
							bind:value={confirmPassword}
							placeholder={m.register_repeat_password()}
							required
							autocomplete="new-password"
							class="w-full rounded-xl border border-[#8FB0C4]/40 bg-[#F9F8F6] py-3.5 pl-12 pr-4 text-sm text-[#2A2E38] outline-none transition-colors placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] focus:bg-white"
						/>
					</div>

					{#if confirmPassword && !passwordsMatch}
						<p class="mt-2 text-xs text-red-600">
							{m.register_password_mismatch()}
						</p>
					{/if}
				</div>

				<label class="flex cursor-pointer items-center gap-3 text-sm text-[#2A2E38]/75">
					<input
						type="checkbox"
						bind:checked={showPassword}
						class="h-4 w-4 accent-[#62AA97]"
					/>
					{m.register_show_password()}
				</label>

				{#if error}
					<p role="alert" class="rounded-xl border border-red-200 bg-red-50 px-4 py-3 text-sm text-red-600">
						{translateError(error)}
					</p>
				{/if}

				<button
					type="submit"
					disabled={loading || !role || !passwordsMatch}
					class="group mt-2 flex w-full items-center justify-center gap-3 rounded-xl bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition-all duration-200 hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-60"
				>
					{loading ? m.register_loading() : m.register_button()}

					<ArrowUpRight
						size={19}
						strokeWidth={1.7}
						class="transition-transform duration-200 group-hover:-translate-y-0.5 group-hover:translate-x-0.5"
					/>
				</button>
			</form>

			<div class="mt-10 border-t border-[#2A2E38]/10 pt-7">
				<p class="text-center text-sm text-[#2A2E38]/60">
					{m.register_have_account()}

					<a
						href={resolve('/auth/login')}
						class="ml-1 inline-flex items-center gap-1 font-semibold text-[#5B9F8D] transition-colors hover:text-[#2A2E38]"
					>
						{m.nav_login()}
						<ArrowRight size={15} />
					</a>
				</p>
			</div>
		</div>
	</div>
</section>
