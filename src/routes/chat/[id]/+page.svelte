<script>
	import { onMount } from 'svelte';
	import { goto } from '$app/navigation';
	import { page } from '$app/state';
	import { resolve } from '$app/paths';
	import { API_URL } from '$lib/api.js';

	let messages = $state([]);
	let partner = $state(null);
	let currentUserId = $state(null);
	let newMessage = $state('');
	let loading = $state(true);
	let sending = $state(false);
	let error = $state('');

	const partnerId = Number(page.params.id);

	onMount(() => {
		loadChat();
	});

	async function loadChat() {
		const token = localStorage.getItem('token');

		if (!token) {
			goto(resolve('/auth/login'));
			return;
		}

		try {
			const headers = {
				Authorization: `Bearer ${token}`
			};

			const [userResponse, partnerResponse, messagesResponse] = await Promise.all([
				fetch(`${API_URL}/api/auth/me`, { headers }),
				fetch(`${API_URL}/api/users/${partnerId}`),
				fetch(`${API_URL}/api/messages/${partnerId}`, { headers })
			]);

			if (!userResponse.ok || !partnerResponse.ok || !messagesResponse.ok) {
				error = 'Chat konnte nicht geladen werden.';
				return;
			}

			const user = await userResponse.json();
			partner = await partnerResponse.json();
			messages = await messagesResponse.json();

			currentUserId = user.user_id;
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			loading = false;
		}
	}

	async function sendMessage(event) {
		event.preventDefault();

		const content = newMessage.trim();

		if (!content || sending) return;

		const token = localStorage.getItem('token');

		if (!token) {
			goto(resolve('/auth/login'));
			return;
		}

		sending = true;
		error = '';

		try {
			const response = await fetch(`${API_URL}/api/messages/${partnerId}`, {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${token}`
				},
				body: JSON.stringify({
					content
				})
			});

			const data = await response.json();

			if (!response.ok) {
				error = data.error || 'Nachricht konnte nicht gesendet werden.';
				return;
			}

			messages.push({
				message_id: data.message_id,
				sender_id: currentUserId,
				content,
				problem_id: null,
				sent_at: new Date().toISOString()
			});

			newMessage = '';
		} catch {
			error = 'Verbindung zum Server nicht möglich.';
		} finally {
			sending = false;
		}
	}

	function formatTime(date) {
		if (!date) return '';

		return new Date(date).toLocaleTimeString('de-DE', {
			hour: '2-digit',
			minute: '2-digit'
		});
	}
</script>

<svelte:head>
	<title>Chat | NextJob</title>
</svelte:head>

<section class="mx-auto max-w-4xl px-4 py-8">
	<a
		href={resolve('/chat')}
		class="mb-5 inline-flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-gray-900"
	>
		← Zurück zu Nachrichten
	</a>

	{#if loading}
		<p class="text-gray-500">Chat wird geladen...</p>
	{:else if error && !partner}
		<p class="rounded-lg bg-red-50 p-4 text-red-700">
			{error}
		</p>
	{:else}
		<div class="overflow-hidden rounded-xl border border-gray-200 bg-white">
			<div class="flex items-center gap-4 border-b border-gray-200 p-4">
				<div
					class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-gray-200 font-bold text-gray-700"
				>
					{partner?.first_name?.charAt(0) || '?'}
				</div>

				<div>
					<h1 class="font-bold text-gray-900">
						{partner?.first_name}
						{partner?.last_name}
					</h1>

					{#if partner?.location}
						<p class="text-sm text-gray-500">
							{partner.location}
						</p>
					{/if}
				</div>
			</div>

			<div class="flex min-h-125 flex-col gap-4 bg-gray-50 p-4 sm:p-6">
				{#if messages.length === 0}
					<p class="my-auto text-center text-sm text-gray-500">
						Noch keine Nachrichten. Schreibe die erste Nachricht.
					</p>
				{:else}
					{#each messages as message (message.message_id)}
						<div class:flex-row-reverse={message.sender_id === currentUserId} class="flex">
							<div
								class:bg-gray-900={message.sender_id === currentUserId}
								class:text-white={message.sender_id === currentUserId}
								class:bg-white={message.sender_id !== currentUserId}
								class:text-gray-900={message.sender_id !== currentUserId}
								class="max-w-[80%] rounded-2xl border border-gray-200 px-4 py-3 sm:max-w-[65%]"
							>
								<p>{message.content}</p>

								<p
									class:text-gray-300={message.sender_id === currentUserId}
									class:text-gray-400={message.sender_id !== currentUserId}
									class="mt-1 text-right text-xs"
								>
									{formatTime(message.sent_at)}
								</p>
							</div>
						</div>
					{/each}
				{/if}
			</div>

			{#if error}
				<p class="border-t border-gray-200 bg-red-50 px-4 py-2 text-sm text-red-700">
					{error}
				</p>
			{/if}

			<form
				onsubmit={sendMessage}
				class="flex items-center gap-3 border-t border-gray-200 bg-white p-4"
			>
				<input
					type="text"
					bind:value={newMessage}
					placeholder="Nachricht schreiben..."
					autocomplete="off"
					class="min-w-0 flex-1 rounded-lg border border-gray-300 px-4 py-3"
				/>

				<button
					type="submit"
					disabled={sending || !newMessage.trim()}
					class="rounded-lg bg-gray-900 px-5 py-3 font-medium text-white hover:bg-gray-700 disabled:cursor-not-allowed disabled:opacity-50"
				>
					{sending ? 'Wird gesendet...' : 'Senden'}
				</button>
			</form>
		</div>
	{/if}
</section>
