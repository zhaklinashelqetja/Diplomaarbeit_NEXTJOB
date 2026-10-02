<script>
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>E-Mail bestätigen | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<div class="rounded-xl border border-[#8FB0C4]/30 bg-white p-8">
		<div class="text-5xl">✉️</div>

		<h1 class="mt-5 text-3xl font-bold text-[#2A2E38]">Überprüfe deine E-Mails</h1>

		<p class="mt-4 text-[#2A2E38]/70">
			Wir haben dir eine E-Mail mit einem Verifizierungslink gesendet. Klicke auf den Link, um dein
			NextJob-Konto zu bestätigen.
		</p>

		<p class="mt-4 text-sm text-[#2A2E38]/50">
			Überprüfe auch deinen Spam-Ordner, falls du keine E-Mail findest.
		</p>

		<a
			href={resolve('/auth/login')}
			class="mt-8 inline-block rounded-lg bg-[#8FB0C4] px-5 py-3 font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
		>
			Zum Login
		</a>
	</div>
</section>
