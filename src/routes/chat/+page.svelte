
<script>
    import { onMount } from 'svelte';
    import { goto } from '$app/navigation';
    import { resolve } from '$app/paths';
    import { ArrowUpRight, MessageCircle, ArrowRight, Inbox } from '@lucide/svelte';
    import { API_URL, localizedUrl } from '$lib/api.js';
    import * as m from '$lib/paraglide/messages.js';
    import { getLocale } from '$lib/paraglide/runtime.js';

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
            const response = await fetch(localizedUrl(`${API_URL}/api/messages/conversations`), {
                headers: {
                    Authorization: `Bearer ${token}`
                }
            });

            const data = await response.json();

            if (!response.ok) {
                error = data.error || 'chat_load_error';
                return;
            }

            conversations = data;
        } catch {
            error = 'chat_server_error';
        } finally {
            loading = false;
        }
    }

    function formatTime(date) {
        if (!date) return '';

        return new Date(date).toLocaleString(getLocale() === 'sq' ? 'sq-AL' : getLocale() === 'en' ? 'en-GB' : 'de-AT', {
            day: '2-digit',
            month: '2-digit',
            hour: '2-digit',
            minute: '2-digit'
        });
    }

    function displayError(value) {
        if (value === 'chat_load_error') {
            return m.chat_load_error();
        }

        if (value === 'chat_server_error') {
            return m.chat_server_error();
        }

        // Fehlermeldungen vom Backend unverändert anzeigen
        return value;
    }
</script>

<svelte:head>
    <title>{m.chat_title()} | NextJob</title>
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">

    <main class="mx-auto max-w-7xl px-5 py-10 sm:px-8 sm:py-16">

        <!-- Header -->
        <section class="border-b border-[#2A2E38]/15 pb-10 sm:pb-14">

            <div class="flex flex-col justify-between gap-8 md:flex-row md:items-end">

                <div class="max-w-3xl">

                    <p class="mb-6 flex items-center gap-3 text-xs font-semibold uppercase tracking-[0.2em] text-[#2A2E38]/55">
                        <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                        NEXTJOB / {m.chat_title()}
                    </p>

                    <h1 class="text-5xl font-semibold leading-[1.08] tracking-tight sm:text-6xl lg:text-7xl">
                        {m.chat_title()}<span class="text-[#62AA97]">.</span>
                    </h1>

                    <p class="mt-6 max-w-xl text-base leading-8 text-[#2A2E38]/60 sm:text-lg">
                        {m.chat_description()}
                    </p>

                </div>

                <div class="flex items-center gap-4 border-l-2 border-[#62AA97] pl-5">

                    <div class="flex h-12 w-12 items-center justify-center bg-[#E8EAE4] text-[#2A2E38]">
                        <MessageCircle size={25} strokeWidth={1.5} />
                    </div>

                    <div>
                        <p class="text-xs uppercase tracking-[0.15em] text-[#2A2E38]/45">
                            NEXTJOB
                        </p>
                        <p class="mt-1 text-sm font-semibold">
                            {m.chat_title()}
                        </p>
                    </div>

                </div>

            </div>

        </section>

        <!-- Conversations -->
        <section class="py-10 sm:py-14">

            <div class="mb-8 flex flex-wrap items-end justify-between gap-5">

                <div>
                    <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                        01 / {m.chat_title()}
                    </p>

                    <h2 class="mt-3 text-2xl font-semibold tracking-tight sm:text-3xl">
                        {m.chat_title()}
                    </h2>
                </div>

                <span class="flex h-11 w-11 items-center justify-center bg-[#E8EAE4]">
                    <Inbox size={22} strokeWidth={1.5} />
                </span>

            </div>

            {#if loading}

                <div class="border-t border-[#2A2E38]/15 py-12">

                    <div class="flex items-center gap-4">

                        <div class="h-5 w-5 animate-spin rounded-full border-2 border-[#62AA97] border-t-transparent"></div>

                        <p class="text-sm text-[#2A2E38]/55">
                            {m.chat_loading()}
                        </p>

                    </div>

                </div>

            {:else if error}

                <div class="border-l-4 border-red-400 bg-red-50 px-6 py-5 text-sm text-red-700">
                    {displayError(error)}
                </div>

            {:else if conversations.length === 0}

                <div class="border border-[#2A2E38]/10 bg-white px-6 py-16 text-center sm:py-20">

                    <div class="mx-auto flex h-16 w-16 items-center justify-center bg-[#E8EAE4]">
                        <MessageCircle size={30} strokeWidth={1.3} />
                    </div>

                    <p class="mx-auto mt-7 max-w-md text-base leading-7 text-[#2A2E38]/60">
                        {m.chat_empty()}
                    </p>

                    <div class="mx-auto mt-8 h-1 w-12 bg-[#62AA97]"></div>

                </div>

            {:else}

                <div class="border-t border-[#2A2E38]/15">

                    {#each conversations as conversation (conversation.partner_id)}

                        <a
                            href={resolve(`/chat/${conversation.partner_id}`)}
                            class="group flex items-center gap-4 border-b border-[#2A2E38]/10 px-3 py-6 transition duration-200 hover:bg-[#E8EAE4] sm:gap-6 sm:px-6"
                        >

                            <!-- Avatar -->
                            <div class="flex h-14 w-14 shrink-0 items-center justify-center bg-[#A8B79E]/35 text-xl font-semibold text-[#2A2E38] sm:h-16 sm:w-16">
                                {conversation.partner.charAt(0)}
                            </div>

                            <!-- Conversation information -->
                            <div class="min-w-0 flex-1">

                                <div class="flex flex-wrap items-center justify-between gap-3">

                                    <h3 class="truncate text-base font-semibold tracking-tight sm:text-lg">
                                        {conversation.partner}
                                    </h3>

                                    <span class="shrink-0 text-xs text-[#2A2E38]/45">
                                        {formatTime(conversation.sent_at)}
                                    </span>

                                </div>

                                <!-- ORIGINALNACHRICHT BLEIBT UNVERÄNDERT -->
                                <p class="mt-2 truncate text-sm leading-6 text-[#2A2E38]/55">
                                    {conversation.last_message_localized ?? conversation.last_message}
                                </p>

                            </div>

                            <!-- Unread messages -->
                            {#if conversation.unread > 0}
                                <span class="flex h-7 min-w-7 shrink-0 items-center justify-center bg-[#2A2E38] px-2 text-xs font-semibold text-white">
                                    {conversation.unread}
                                </span>
                            {/if}

                            <ArrowUpRight
                                size={22}
                                strokeWidth={1.5}
                                class="hidden shrink-0 text-[#2A2E38]/40 transition group-hover:text-[#62AA97] sm:block"
                            />

                        </a>

                    {/each}

                </div>

            {/if}

        </section>

        <!-- Footer -->
        <footer class="flex flex-wrap items-center justify-between gap-4 border-t border-[#2A2E38]/15 py-6">

            <p class="text-xs font-semibold tracking-[0.12em]">
                NEXTJOB
            </p>

            <div class="flex items-center gap-2 text-xs text-[#2A2E38]/45">
                <span>{m.chat_title()}</span>
                <ArrowRight size={14} />
                <span>Shkodër</span>
            </div>

        </footer>

    </main>

</div>
