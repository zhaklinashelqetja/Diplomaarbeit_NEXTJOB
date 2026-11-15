<script>
	import { resolve } from '$app/paths';
	import { t } from '$lib/i18n.js';
</script>

<footer class="border-t border-[#8FB0C4]/30 bg-[#8FB0C4]/15">
	<div
		class="mx-auto flex max-w-6xl flex-col items-center justify-between gap-3 px-4 py-3 sm:flex-row"
	>
		<div class="flex items-center gap-2">
			<img src="/images/nextjob-logo.png" alt="NextJob Logo" class="h-7 w-auto" />

			<p class="text-xs text-[#2A2E38]/60">
				© {new Date().getFullYear()} NextJob · Shkodër
			</p>
		</div>

		<div class="flex gap-5">
			<a
				href={resolve('/wer-wir-sind')}
				class="text-xs text-[#2A2E38]/70 hover:text-[#62AA97]"
			>
				{$t('footer_ueber_uns')}
			</a>

			<a
				href={resolve('/kontakt')}
				class="text-xs text-[#2A2E38]/70 hover:text-[#62AA97]"
			>
				{$t('footer_kontakt')}
			</a>
		</div>
	</div>
</footer>