<script>
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
</script>

<svelte:head>
	<title>NextJob | {$t('home_badge')}</title>
	<meta
		name="description"
		content="NextJob verbindet Auftraggeber mit lokalen Dienstleistern und Handwerkern in Shkodër."
	/>
</svelte:head>

<!-- HERO -->
<section class="relative overflow-hidden bg-[#F5F1EE]">
	<!-- Dekoration -->
	<div class="absolute -top-24 -right-24 h-72 w-72 rounded-full bg-[#8FB0C4]/25 blur-3xl"></div>
	<div class="absolute -bottom-24 -left-24 h-72 w-72 rounded-full bg-[#A8B79E]/25 blur-3xl"></div>

	<div
		class="relative mx-auto flex max-w-6xl flex-col items-center px-4 py-20 text-center md:py-28"
	>
		<div
			class="mb-5 rounded-full border border-[#8FB0C4]/50 bg-[#8FB0C4]/15 px-4 py-2 text-sm font-semibold text-[#2A2E38]"
		>
			{$t('home_badge')}
		</div>

		<h1
			class="max-w-4xl text-5xl leading-tight font-bold tracking-tight text-[#2A2E38] md:text-7xl"
			style="font-family: var(--font-heading);"
		>
			{$t('home_title1')}
			<span class="text-[#62AA97]">{$t('home_title2')}</span>
		</h1>

		<p class="mt-6 max-w-2xl text-lg leading-relaxed text-[#2A2E38]/70 md:text-xl">
			{$t('home_description')}
		</p>

		<div class="mt-9 flex w-full flex-col justify-center gap-3 sm:w-auto sm:flex-row">
			<a
				href={resolve('/auth/register')}
				class="rounded-xl bg-[#2A2E38] px-7 py-3.5 font-semibold text-[#F5F1EE] transition hover:-translate-y-0.5 hover:bg-[#62AA97]"
			>
				{$t('home_start')}
			</a>

			<a
				href={resolve('/wer-wir-sind')}
				class="rounded-xl border border-[#8FB0C4] bg-white/60 px-7 py-3.5 font-semibold text-[#2A2E38] transition hover:-translate-y-0.5 hover:bg-[#8FB0C4]/20"
			>
				{$t('home_more')}
			</a>
		</div>
	</div>
</section>

<!-- FÜR WEN IST NEXTJOB? -->
<section class="bg-white/60">
	<div class="mx-auto max-w-6xl px-4 py-16 md:py-20">
		<div class="grid gap-5 md:grid-cols-2">
			<div class="rounded-2xl border border-[#8FB0C4]/30 bg-[#8FB0C4]/15 p-7 md:p-9">
				<div
					class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-[#8FB0C4] text-xl"
				>
					🔎
				</div>

				<h2 class="text-2xl font-bold text-[#2A2E38]">{$t('home_need_help')}</h2>

				<p class="mt-3 leading-relaxed text-[#2A2E38]/70">
					{$t('home_need_help_desc')}
				</p>

				<a
					href={resolve('/auth/register')}
					class="mt-5 inline-block font-semibold text-[#2A2E38] hover:text-[#62AA97]"
				>
					{$t('home_create_job')} →
				</a>
			</div>

			<div class="rounded-2xl border border-[#A8B79E]/40 bg-[#A8B79E]/15 p-7 md:p-9">
				<div
					class="mb-5 flex h-12 w-12 items-center justify-center rounded-xl bg-[#A8B79E] text-xl"
				>
					🛠️
				</div>

				<h2 class="text-2xl font-bold text-[#2A2E38]">{$t('home_need_work')}</h2>

				<p class="mt-3 leading-relaxed text-[#2A2E38]/70">
					{$t('home_need_work_desc')}
				</p>

				<a
					href={resolve('/auth/register')}
					class="mt-5 inline-block font-semibold text-[#2A2E38] hover:text-[#62AA97]"
				>
					{$t('home_find_work')} →
				</a>
			</div>
		</div>
	</div>
</section>

<!-- WIE FUNKTIONIERT NEXTJOB? -->
<section class="bg-[#F5F1EE]">
	<div class="mx-auto max-w-6xl px-4 py-16 md:py-20">
		<div class="text-center">
			<p class="font-semibold text-[#62AA97]">{$t('home_how')}</p>

			<h2 class="mt-2 text-3xl font-bold text-[#2A2E38] md:text-4xl">
				{$t('home_steps_title')}
			</h2>

			<p class="mt-3 text-[#2A2E38]/65">{$t('home_steps_desc')}</p>
		</div>

		<div class="mt-12 grid gap-6 md:grid-cols-3">
			<div
				class="rounded-2xl border border-[#8FB0C4]/30 bg-white p-7 transition hover:-translate-y-1"
			>
				<div
					class="flex h-11 w-11 items-center justify-center rounded-full bg-[#8FB0C4]/25 font-bold text-[#2A2E38]"
				>
					01
				</div>

				<h3 class="mt-5 text-xl font-bold text-[#2A2E38]">{$t('home_step1')}</h3>

				<p class="mt-3 leading-relaxed text-[#2A2E38]/65">
					{$t('home_step1_desc')}
				</p>
			</div>

			<div
				class="rounded-2xl border border-[#A8B79E]/40 bg-white p-7 transition hover:-translate-y-1"
			>
				<div
					class="flex h-11 w-11 items-center justify-center rounded-full bg-[#A8B79E]/30 font-bold text-[#2A2E38]"
				>
					02
				</div>

				<h3 class="mt-5 text-xl font-bold text-[#2A2E38]">{$t('home_step2')}</h3>

				<p class="mt-3 leading-relaxed text-[#2A2E38]/65">
					{$t('home_step2_desc')}
				</p>
			</div>

			<div
				class="rounded-2xl border border-[#62AA97]/30 bg-white p-7 transition hover:-translate-y-1"
			>
				<div
					class="flex h-11 w-11 items-center justify-center rounded-full bg-[#62AA97]/20 font-bold text-[#2A2E38]"
				>
					03
				</div>

				<h3 class="mt-5 text-xl font-bold text-[#2A2E38]">{$t('home_step3')}</h3>

				<p class="mt-3 leading-relaxed text-[#2A2E38]/65">
					{$t('home_step3_desc')}
				</p>
			</div>
		</div>
	</div>
</section>

<!-- CTA -->
<section class="bg-[#8FB0C4]">
	<div class="mx-auto max-w-6xl px-4 py-14 text-center md:py-16">
		<h2 class="text-3xl font-bold text-[#2A2E38] md:text-4xl">{$t('home_cta_title')}</h2>

		<p class="mx-auto mt-3 max-w-xl text-[#2A2E38]/75">
			{$t('home_cta_desc')}
		</p>

		<a
			href={resolve('/auth/register')}
			class="mt-7 inline-block rounded-xl bg-[#2A2E38] px-7 py-3.5 font-semibold text-[#F5F1EE] transition hover:-translate-y-0.5 hover:bg-[#F5F1EE] hover:text-[#2A2E38]"
		>
			{$t('home_cta_button')}
		</a>
	</div>
</section>