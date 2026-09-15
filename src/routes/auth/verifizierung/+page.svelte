<script>
	import { resolve } from '$app/paths';
</script>

<svelte:head>
	<title>E-Mail bestätigen | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-md px-4 py-16 text-center">
	<div class="rounded-xl border border-gray-200 bg-white p-8">
		<div class="text-5xl">✉️</div>

		<h1 class="mt-5 text-3xl font-bold text-gray-900">Überprüfe deine E-Mails</h1>

		<p class="mt-4 text-gray-600">
			Wir haben dir eine E-Mail mit einem Verifizierungslink gesendet. Klicke auf den Link, um dein
			NextJob-Konto zu bestätigen.
		</p>

		<p class="mt-4 text-sm text-gray-500">
			Überprüfe auch deinen Spam-Ordner, falls du keine E-Mail findest.
		</p>

		<a
			href={resolve('/auth/login')}
			class="mt-8 inline-block rounded-lg bg-gray-900 px-5 py-3 font-medium text-white hover:bg-gray-700"
		>
			Zum Login
		</a>
	</div>
</section>
