<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';

	let conversations = $state([]);
	let loading = $state(true);
	let error = $state('');

	onMount(() => {
		loadConversations();
	});

	async function loadConversations() {
		const token = localStorage.getItem('token');

		if (!token) {
			goto(resolve('/auth/login'));
			return;
		}

		try {
			const response = await fetch(`${API_URL}/api/messages/conversations`, {
				headers: {
					Authorization: `Bearer ${token}`
				}
			});

			const data = await response.json();

			if (!response.ok) {
				error = data.error || 'Nachrichten konnten nicht geladen werden.';
				return;
			}

			conversations = data;
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}

	function formatTime(date) {
		if (!date) return '';

		return new Date(date).toLocaleString('de-DE', {
			day: '2-digit',
			month: '2-digit',
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>Nachrichten | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-4xl px-4 py-12">
	<h1 class="text-3xl font-bold text-gray-900">Nachrichten</h1>

	<p class="mt-2 text-gray-600">Deine Gespräche mit Auftraggebern und Dienstleistern.</p>

	{#if loading}
		<p class="mt-8 text-gray-500">Nachrichten werden geladen...</p>
	{:else if error}
		<p class="mt-8 rounded-lg bg-red-50 p-4 text-red-700">
			{error}
		</p>
	{:else if conversations.length === 0}
		<div class="mt-8 rounded-xl border border-gray-200 bg-white p-8 text-center">
			<p class="text-gray-600">Du hast noch keine Nachrichten.</p>
		</div>
	{:else}
		<div class="mt-8 overflow-hidden rounded-xl border border-gray-200 bg-white">
			{#each conversations as conversation (conversation.partner_id)}
				<a
					href={resolve(`/chat/${conversation.partner_id}`)}
					class="flex w-full items-center gap-4 border-b border-gray-200 p-4 text-left last:border-b-0 hover:bg-gray-50"
				>
					<div
						class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gray-200 font-semibold text-gray-700"
					>
						{conversation.partner.charAt(0)}
					</div>

					<div class="min-w-0 flex-1">
						<div class="flex items-center justify-between gap-3">
							<h2 class="truncate font-semibold text-gray-900">
								{conversation.partner}
							</h2>

							<span class="shrink-0 text-xs text-gray-500">
								{formatTime(conversation.sent_at)}
							</span>
						</div>

						<p class="mt-1 truncate text-sm text-gray-500">
							{conversation.last_message}
						</p>
					</div>

					{#if conversation.unread > 0}
						<span
							class="flex h-6 min-w-6 items-center justify-center rounded-full bg-gray-900 px-2 text-xs font-medium text-white"
						>
							{conversation.unread}
						</span>
					{/if}
				</a>
			{/each}
		</div>
	{/if}
</section>
