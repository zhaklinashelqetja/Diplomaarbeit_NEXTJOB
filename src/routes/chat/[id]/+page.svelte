
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { page } from '$app/state';
    import { resolve } from '$app/paths';
    import {
        ArrowLeft,
        ArrowUpRight,
        MapPin,
        Send,
        MessageCircle
    } from '@lucide/svelte';
    import { API_URL, localizedUrl } from '$lib/api.js';
    import * as m from '$lib/paraglide/messages.js';
    import { getLocale } from '$lib/paraglide/runtime.js';

    let messages = $state([]);
    let partner = $state(null);
    let currentUserId = $state(null);
    let newMessage = $state('');
    let loading = $state(true);
    let sending = $state(false);
    let error = $state('');

    const partnerId = Number(page.params.id);

    let active = false;
    let refreshInProgress = false;
    let refreshTimer;

    onMount(() => {
        active = true;

        loadChat().then((success) => {
            if (!active || !success) return;

            refreshTimer = setInterval(() => {
                if (document.visibilityState === 'visible') {
                    refreshMessages();
                }
            }, 3000);
        });

        return () => {
            active = false;
            clearInterval(refreshTimer);
        };
    });

    async function loadChat() {
        const token = localStorage.getItem('token');

        if (!token) {
            goto(resolve('/auth/login'));
            loading = false;
            return false;
        }

        try {
            const headers = {
                Authorization: `Bearer ${token}`
            };

            const [
                userResponse,
                partnerResponse,
                messagesResponse
            ] = await Promise.all([
                fetch(localizedUrl(`${API_URL}/api/auth/me`), { headers }),
                fetch(localizedUrl(`${API_URL}/api/users/${partnerId}`)),
                fetch(localizedUrl(`${API_URL}/api/messages/${partnerId}`), {
                    headers
                })
            ]);

            if (
                !userResponse.ok ||
                !partnerResponse.ok ||
                !messagesResponse.ok
            ) {
                if (active) error = 'chat_load_failed';
                return false;
            }

            const user = await userResponse.json();
            const partnerData = await partnerResponse.json();
            const messageData = await messagesResponse.json();

            if (!Array.isArray(messageData)) {
                if (active) error = 'chat_load_failed';
                return false;
            }

            if (!active) return false;

            currentUserId = user.user_id;
            partner = partnerData;
            messages = messageData;

            return true;
        } catch {
            if (active) error = 'chat_server_error';
            return false;
        } finally {
            if (active) loading = false;
        }
    }

    async function refreshMessages() {
        if (!active || refreshInProgress || sending) return;

        const token = localStorage.getItem('token');

        if (!token) {
            clearInterval(refreshTimer);
            goto(resolve('/auth/login'));
            return;
        }

        refreshInProgress = true;

        try {
            const response = await fetch(
                localizedUrl(`${API_URL}/api/messages/${partnerId}`),
                {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                }
            );

            if (response.status === 401) {
                clearInterval(refreshTimer);
                if (active) {
                    error = 'chat_load_failed';
                }
                return;
            }

            if (!response.ok) return;

            const updatedMessages = await response.json();

            if (!active || !Array.isArray(updatedMessages)) return;

            const existingIds = new Set(
                messages.map((message) => message.message_id)
            );

            const newIncomingMessages = updatedMessages.filter(
                (message) => !existingIds.has(message.message_id)
            );

            if (newIncomingMessages.length > 0) {
                const combined = new Map();

                for (const message of messages) {
                    combined.set(message.message_id, message);
                }

                for (const message of updatedMessages) {
                    combined.set(message.message_id, message);
                }

                messages = [...combined.values()].sort(
                    (a, b) => a.message_id - b.message_id
                );
            }
        } catch {
            // Ein fehlgeschlagener Hintergrundabruf
            // unterbricht den Chat nicht.
        } finally {
            refreshInProgress = false;
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
            const response = await fetch(
                localizedUrl(`${API_URL}/api/messages/${partnerId}`),
                {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        Authorization: `Bearer ${token}`
                    },
                    body: JSON.stringify({ content })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                error = data.error || 'chat_send_failed';
                return;
            }

            if (!active) return;

            if (
                !messages.some(
                    (message) => message.message_id === data.message_id
                )
            ) {
                messages = [
                    ...messages,
                    {
                        message_id: data.message_id,
                        sender_id: currentUserId,
                        content,
                        problem_id: null,
                        sent_at: new Date().toISOString()
                    }
                ];
            }

            newMessage = '';
        } catch {
            if (active) error = 'chat_server_error';
        } finally {
            sending = false;
        }
    }

    function formatTime(date) {
        if (!date) return '';

        return new Date(date).toLocaleTimeString(
            getLocale() === 'sq' ? 'sq-AL' : getLocale() === 'en' ? 'en-GB' : 'de-AT',
            {
                hour: '2-digit',
                minute: '2-digit'
            }
        );
    }

    function displayError(value) {
        if (value === 'chat_load_failed') {
            return m.chat_load_failed();
        }

        if (value === 'chat_send_failed') {
            return m.chat_send_failed();
        }

        if (value === 'chat_server_error') {
            return m.chat_server_error();
        }

        return value;
    }
</script>

<svelte:head>
    <title>Chat | NextJob</title>
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-14">

        <!-- Back navigation -->
        <a
            href={resolve('/chat')}
            class="group mb-10 inline-flex items-center gap-3 text-xs font-semibold uppercase tracking-[0.15em] text-[#2A2E38]/65 transition hover:text-[#62AA97]"
        >
            <ArrowLeft
                size={19}
                strokeWidth={1.5}
                class="transition-transform group-hover:-translate-x-1"
            />
            {m.chat_back()}
        </a>

        <!-- Page heading -->
        <section class="mb-10 border-b border-[#2A2E38]/15 pb-10">
            <div class="flex flex-wrap items-end justify-between gap-6">
                <div>
                    <p class="mb-5 flex items-center gap-3 text-xs font-semibold uppercase tracking-[0.2em] text-[#2A2E38]/50">
                        <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                        NEXTJOB / CHAT
                    </p>

                    <h1 class="text-4xl font-semibold tracking-tight sm:text-5xl lg:text-6xl">
                        {m.chat_title()}<span class="text-[#62AA97]">.</span>
                    </h1>
                </div>

                <div class="flex items-center gap-3 border-l-2 border-[#62AA97] pl-5">
                    <MessageCircle size={25} strokeWidth={1.5} />
                    <span class="text-xs font-semibold uppercase tracking-[0.12em]">
                        NEXTJOB
                    </span>
                </div>
            </div>
        </section>

        {#if loading}
            <div class="flex min-h-80 items-center justify-center gap-4 border border-[#2A2E38]/10 bg-white">
                <div class="h-5 w-5 animate-spin rounded-full border-2 border-[#62AA97] border-t-transparent"></div>

                <p class="text-sm text-[#2A2E38]/55">
                    {m.chat_loading_conversation()}
                </p>
            </div>

        {:else if error && !partner}
            <div class="border-l-4 border-red-400 bg-red-50 px-6 py-5 text-sm text-red-700">
                {displayError(error)}
            </div>

        {:else}
            <section class="overflow-hidden border border-[#2A2E38]/10 bg-white">

                <!-- Partner header -->
                <div class="flex items-center gap-4 border-b border-[#2A2E38]/10 bg-white px-5 py-6 sm:gap-5 sm:px-8">
                    <div class="flex h-14 w-14 shrink-0 items-center justify-center bg-[#A8B79E]/35 text-xl font-semibold sm:h-16 sm:w-16">
                        {partner?.first_name?.charAt(0) || '?'}
                    </div>

                    <div class="min-w-0 flex-1">
                        <h2 class="truncate text-lg font-semibold tracking-tight sm:text-xl">
                            {partner?.first_name}
                            {partner?.last_name}
                        </h2>

                        {#if partner?.neighborhood}
                            <p class="mt-2 flex items-center gap-2 text-sm text-[#2A2E38]/50">
                                <MapPin size={15} strokeWidth={1.5} />
                                {partner.neighborhood}
                            </p>
                        {/if}
                    </div>

                    <div class="hidden h-11 w-11 items-center justify-center border border-[#2A2E38]/10 text-[#2A2E38]/50 sm:flex">
                        <ArrowUpRight size={21} strokeWidth={1.5} />
                    </div>
                </div>

                <!-- Messages -->
                <div class="flex min-h-125 flex-col gap-5 bg-[#F8F7F4] px-4 py-8 sm:px-8 sm:py-10">
                    {#if messages.length === 0}
                        <div class="my-auto flex flex-col items-center justify-center py-12 text-center">
                            <div class="flex h-16 w-16 items-center justify-center bg-[#E8EAE4]">
                                <MessageCircle size={29} strokeWidth={1.3} />
                            </div>

                            <p class="mt-6 max-w-sm text-sm leading-7 text-[#2A2E38]/55">
                                {m.chat_empty_conversation()}
                            </p>

                            <div class="mt-7 h-1 w-10 bg-[#62AA97]"></div>
                        </div>
                    {:else}
                        {#each messages as message (message.message_id)}
                            <div
                                class:flex-row-reverse={message.sender_id === currentUserId}
                                class="flex"
                            >
                                <div
                                    class={`max-w-[85%] border px-5 py-4 sm:max-w-[65%] ${
                                        message.sender_id === currentUserId
                                            ? 'border-transparent bg-[#2A2E38] text-white'
                                            : 'border-[#2A2E38]/10 bg-white text-[#2A2E38]'
                                    }`}
                                >
                                    <p class="wrap-break-word whitespace-pre-wrap text-sm leading-7">
                                        {message.content}
                                    </p>

                                    <p
                                        class:text-gray-400={message.sender_id === currentUserId}
                                        class:text-gray-500={message.sender_id !== currentUserId}
                                        class="mt-3 text-right text-[11px]"
                                    >
                                        {formatTime(message.sent_at)}
                                    </p>
                                </div>
                            </div>
                        {/each}
                    {/if}
                </div>

                <!-- Error -->
                {#if error}
                    <p class="border-t border-red-100 bg-red-50 px-5 py-4 text-sm text-red-700 sm:px-8">
                        {displayError(error)}
                    </p>
                {/if}

                <!-- Message form -->
                <form
                    onsubmit={sendMessage}
                    class="border-t border-[#2A2E38]/10 bg-white p-4 sm:p-6"
                >
                    <div class="flex items-center gap-3">
                        <input
                            type="text"
                            bind:value={newMessage}
                            placeholder={m.chat_message_placeholder()}
                            autocomplete="off"
                            class="min-w-0 flex-1 border border-[#2A2E38]/15 bg-[#F8F7F4] px-4 py-4 text-sm text-[#2A2E38] outline-none transition placeholder:text-[#2A2E38]/35 focus:border-[#62AA97] sm:px-5"
                        />

                        <button
                            type="submit"
                            disabled={sending || !newMessage.trim()}
                            class="flex shrink-0 items-center justify-center gap-3 bg-[#2A2E38] px-5 py-4 text-sm font-semibold text-white transition hover:bg-[#62AA97] disabled:cursor-not-allowed disabled:opacity-50 sm:px-7"
                        >
                            <span class="hidden sm:inline">
                                {sending ? m.chat_sending() : m.chat_send()}
                            </span>

                            <Send size={18} strokeWidth={1.7} />
                        </button>
                    </div>
                </form>
            </section>
        {/if}

        <!-- Footer -->
        <footer class="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-[#2A2E38]/15 py-6">
            <p class="text-xs font-semibold tracking-[0.12em]">
                NEXTJOB
            </p>

            <p class="text-xs text-[#2A2E38]/45">
                Shkodër
            </p>
        </footer>
    </main>
</div>
