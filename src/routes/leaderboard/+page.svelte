
<script>
    import * as m from '$lib/paraglide/messages.js';
    import { ArrowUpRight, MapPin, Trophy, Star } from '@lucide/svelte';

    let { data } = $props();

    let activeTab = $state('workers');

    let workers = $derived(data.workers ?? []);
    let employers = $derived(data.employers ?? []);

    let currentList = $derived(
        activeTab === 'workers' ? workers : employers
    );

    let topThree = $derived(currentList.slice(0, 3));
    let remainingUsers = $derived(currentList.slice(3));

    function getName(user) {
        return (
            `${user.first_name ?? ''} ${user.last_name ?? ''}`.trim() ||
            user.name ||
            m.leaderboard_user()
        );
    }

    function getInitials(user) {
        const first = user.first_name ?? '';
        const last = user.last_name ?? '';
        return `${first.charAt(0)}${last.charAt(0)}`.toUpperCase() || '?';
    }

    function getScore(user) {
        return user.score ?? user.points ?? 0;
    }

    function getRating(user) {
        return Number(user.rating ?? user.average_rating ?? 0).toFixed(1);
    }

    function getReviews(user) {
        return user.review_count ?? user.reviews_count ?? 0;
    }

    function getAvatar(user) {
        return user.avatar_url ?? user.profile_picture ?? user.avatar ?? '';
    }
</script>

<svelte:head>
    <title>{m.leaderboard_seo_title()}</title>
    <meta
        name="description"
        content={m.leaderboard_seo_description()}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38] pb-20">

    <!-- HERO -->
    <section class="px-5 pt-8 sm:px-10 lg:px-16 lg:pt-14">
        <div class="mx-auto grid max-w-7xl grid-cols-1 gap-8 lg:grid-cols-[1.15fr_0.85fr]">

            <!-- HERO TEXT -->
            <div class="relative flex flex-col justify-between overflow-hidden rounded-none bg-[#2A2E38] p-8 text-[#F5F1EE] sm:p-12 lg:min-h-[430px]">

                <div class="absolute -right-24 -top-24 h-80 w-80 rounded-full border border-white/5"></div>
                <div class="absolute -right-16 -top-16 h-64 w-64 rounded-full border border-white/5"></div>
                <div class="absolute bottom-0 right-0 h-64 w-64 bg-[#A8B79E]/5 blur-3xl"></div>

                <div class="relative">
                    <p class="mb-8 flex items-center gap-3 text-xs font-bold uppercase tracking-[3px] text-[#A8B79E]">
                        <span class="h-2 w-2 rounded-full bg-[#A8B79E]"></span>
                        {m.leaderboard_community()}
                    </p>

                    <h1 class="text-5xl font-black leading-[0.95] tracking-[-2px] sm:text-6xl lg:text-7xl">
                        {#if activeTab === 'workers'}
                            {m.leaderboard_top()}
                            <br />
                            <span class="text-[#A8B79E]">{m.leaderboard_hero_workers()}</span>
                        {:else}
                            {m.leaderboard_top()}
                            <br />
                            <span class="text-[#A8B79E]">{m.leaderboard_hero_employers()}</span>
                        {/if}
                    </h1>

                    <p class="mt-7 max-w-md text-sm leading-7 text-[#D5D8DF] sm:text-base">
                        {m.leaderboard_hero_description()}
                    </p>
                </div>

                <div class="relative mt-10 flex items-end justify-between border-t border-white/10 pt-5">
                    <div>
                        <p class="text-xs uppercase tracking-[2px] text-[#A8B79E]">
                            {activeTab === 'workers' ? m.leaderboard_workers() : m.leaderboard_employers()}
                        </p>
                        <p class="mt-2 text-sm text-white/70">
                            {m.leaderboard_members({ count: currentList.length })}
                        </p>
                    </div>

                    <Trophy size={36} strokeWidth={1} class="text-[#A8B79E]" />
                </div>
            </div>

            <!-- HERO SIDE -->
            <div class="relative overflow-hidden rounded-none bg-[#DCE3D8] p-8 sm:p-10 lg:min-h-[430px]">

                <div class="absolute -right-20 -top-20 h-72 w-72 rounded-full bg-[#A8B79E]/40 blur-3xl"></div>

                <div class="relative flex h-full flex-col justify-between">
                    <div class="flex items-start justify-between">
                        <span class="text-xs font-bold uppercase tracking-[2px] text-[#647565]">
                            {m.leaderboard_ranking()}
                        </span>

                        <span class="text-sm text-[#647565]">01 — 03</span>
                    </div>

                    <div class="py-10">
                        <div class="mb-6 flex items-end justify-center gap-3">

                            <!-- SECOND -->
                            <div class="flex flex-col items-center">
                                <div class="mb-3 flex h-16 w-16 items-center justify-center rounded-full border border-[#2A2E38]/10 bg-[#F5F1EE] text-xl font-bold text-[#2A2E38] sm:h-20 sm:w-20">
                                    02
                                </div>
                                <div class="h-24 w-20 bg-[#8FB0C4] sm:h-28 sm:w-28"></div>
                            </div>

                            <!-- FIRST -->
                            <div class="flex flex-col items-center">
                                <div class="mb-3 flex h-20 w-20 items-center justify-center rounded-full border border-[#2A2E38]/10 bg-[#F5F1EE] text-2xl font-black text-[#2A2E38] sm:h-24 sm:w-24">
                                    01
                                </div>
                                <div class="flex h-36 w-24 items-center justify-center bg-[#A8B79E] sm:h-44 sm:w-32">
                                    <Trophy size={44} strokeWidth={1} class="text-[#2A2E38]" />
                                </div>
                            </div>

                            <!-- THIRD -->
                            <div class="flex flex-col items-center">
                                <div class="mb-3 flex h-16 w-16 items-center justify-center rounded-full border border-[#2A2E38]/10 bg-[#F5F1EE] text-xl font-bold text-[#2A2E38] sm:h-20 sm:w-20">
                                    03
                                </div>
                                <div class="h-16 w-20 bg-[#C7A58C] sm:h-20 sm:w-28"></div>
                            </div>
                        </div>

                        <div class="text-center">
                            <h2 class="text-2xl font-black tracking-tight sm:text-3xl">
                                {m.leaderboard_recognition()}<br />{m.leaderboard_performance()}
                            </h2>
                            <p class="mt-3 text-sm text-[#647565]">
                                {m.leaderboard_quality()}
                            </p>
                        </div>
                    </div>

                    <div class="flex items-center justify-between border-t border-[#2A2E38]/10 pt-5">
                        <span class="text-xs uppercase tracking-[2px] text-[#647565]">
                            NEXTJOB
                        </span>

                        <ArrowUpRight size={24} strokeWidth={1.3} />
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- RANKING SECTION -->
    <section class="mx-auto max-w-7xl px-5 pt-20 sm:px-10 lg:px-16 lg:pt-28">

        <!-- SECTION HEADER -->
        <div class="mb-10 flex flex-col gap-6 md:flex-row md:items-end md:justify-between">
            <div>
                <p class="mb-4 text-xs font-bold uppercase tracking-[3px] text-[#7C8D78]">
                    <span class="mr-2">02 /</span> {m.leaderboard_community_ranking()}
                </p>

                <h2 class="text-4xl font-black leading-tight tracking-[-1.5px] sm:text-5xl">
                    {m.leaderboard_best()}<br />
                    <span class="text-[#7C8D78]">{m.leaderboard_field()}</span>
                </h2>
            </div>

            <p class="max-w-sm text-sm leading-7 text-[#747985] md:pb-2">
                {m.leaderboard_description()}
            </p>
        </div>

        <!-- TAB SWITCH -->
        <div class="mb-10 flex flex-wrap items-center gap-3 border-b border-[#DCD6D0] pb-5">
            <button
                onclick={() => activeTab = 'workers'}
                class={`group flex items-center gap-3 border-b-2 px-4 py-3 text-sm font-bold transition-all ${
                    activeTab === 'workers'
                        ? 'border-[#2A2E38] text-[#2A2E38]'
                        : 'border-transparent text-[#858995] hover:text-[#2A2E38]'
                }`}
            >
                <span>01</span>
                {m.leaderboard_workers()}
                <ArrowUpRight size={17} class="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </button>

            <button
                onclick={() => activeTab = 'employers'}
                class={`group flex items-center gap-3 border-b-2 px-4 py-3 text-sm font-bold transition-all ${
                    activeTab === 'employers'
                        ? 'border-[#2A2E38] text-[#2A2E38]'
                        : 'border-transparent text-[#858995] hover:text-[#2A2E38]'
                }`}
            >
                <span>02</span>
                {m.leaderboard_employers()}
                <ArrowUpRight size={17} class="transition-transform group-hover:-translate-y-0.5 group-hover:translate-x-0.5" />
            </button>
        </div>

        <!-- ERROR -->
        {#if !data.leaderboardAvailable}
            <div class="border-y border-[#DCD6D0] py-20 text-center">
                <Trophy size={42} strokeWidth={1} class="mx-auto mb-5 text-[#7C8D78]" />
                <h3 class="text-2xl font-bold">{m.leaderboard_unavailable()}</h3>
                <p class="mt-3 text-sm text-[#747985]">
                    {m.leaderboard_error()}
                </p>
            </div>

        <!-- EMPTY -->
        {:else if currentList.length === 0}
            <div class="border-y border-[#DCD6D0] py-20 text-center">
                <Trophy size={42} strokeWidth={1} class="mx-auto mb-5 text-[#7C8D78]" />
                <h3 class="text-2xl font-bold">{m.leaderboard_empty()}</h3>
                <p class="mt-3 text-sm text-[#747985]">
                    {m.leaderboard_empty_description()}
                </p>
            </div>

        {:else}

            <!-- TOP THREE -->
            {#if topThree.length > 0}
                <div class="mb-16 grid grid-cols-1 gap-6 md:grid-cols-3">

                    {#each topThree as user, i}
                        <article class={`relative overflow-hidden border p-6 sm:p-8 ${
                            i === 0
                                ? 'border-[#A8B79E] bg-[#E9EDE6]'
                                : i === 1
                                    ? 'border-[#DCD6D0] bg-[#FAF8F5]'
                                    : 'border-[#DCD6D0] bg-[#FAF8F5]'
                        }`}>

                            <div class="mb-7 flex items-center justify-between">
                                <span class="text-xs font-bold uppercase tracking-[2px] text-[#747985]">
                                    {m.leaderboard_rank()} / 0{i + 1}
                                </span>

                                {#if i === 0}
                                    <Trophy size={23} strokeWidth={1.3} class="text-[#7C8D78]" />
                                {:else}
                                    <ArrowUpRight size={22} strokeWidth={1.2} class="text-[#858995]" />
                                {/if}
                            </div>

                            <!-- PROFILE -->
                            <div class="flex items-center gap-5">

                                {#if getAvatar(user)}
                                    <img
                                        src={getAvatar(user)}
                                        alt={getName(user)}
                                        class="h-20 w-20 rounded-full object-cover"
                                    />
                                {:else}
                                    <div class={`flex h-20 w-20 shrink-0 items-center justify-center rounded-full text-xl font-black ${
                                        i === 0
                                            ? 'bg-[#A8B79E] text-[#2A2E38]'
                                            : 'bg-[#E4DED8] text-[#2A2E38]'
                                    }`}>
                                        {getInitials(user)}
                                    </div>
                                {/if}

                                <div class="min-w-0">
                                    <h3 class="break-words text-xl font-black tracking-tight">
                                        {getName(user)}
                                    </h3>

                                    {#if user.location}
                                        <p class="mt-2 flex items-center gap-1.5 text-xs text-[#747985]">
                                            <MapPin size={14} />
                                            {user.location}
                                        </p>
                                    {/if}
                                </div>
                            </div>

                            <!-- RATING -->
                            <div class="mt-8 flex items-center justify-between border-t border-[#2A2E38]/10 pt-5">
                                <div>
                                    <p class="mb-2 text-xs uppercase tracking-[1.5px] text-[#747985]">
                                        {m.leaderboard_rating()}
                                    </p>

                                    <div class="flex items-center gap-2">
                                        <Star size={17} fill="#D8AA53" stroke="#D8AA53" />
                                        <span class="text-lg font-bold">{getRating(user)}</span>
                                        <span class="text-xs text-[#858995]">
                                            ({getReviews(user)})
                                        </span>
                                    </div>
                                </div>

                                <div class="text-right">
                                    <p class="mb-2 text-xs uppercase tracking-[1.5px] text-[#747985]">
                                        {m.leaderboard_points()}
                                    </p>

                                    <span class="text-3xl font-black tracking-tight text-[#7C8D78]">
                                        {getScore(user)}
                                    </span>
                                </div>
                            </div>

                            <div class="mt-6 flex items-center justify-between border-t border-[#2A2E38]/10 pt-4">
                                <span class="text-xs font-bold uppercase tracking-[2px]">
                                    {i === 0 ? m.leaderboard_top_performer() : m.leaderboard_position({ position: i + 1 })}
                                </span>

                                <span class="text-xs text-[#747985]">
                                    NEXTJOB
                                </span>
                            </div>
                        </article>
                    {/each}
                </div>
            {/if}

            <!-- REST OF LIST -->
            {#if remainingUsers.length > 0}
                <div class="border-t border-[#DCD6D0]">

                    <!-- HEADER -->
                    <div class="grid grid-cols-[50px_1fr_100px] gap-4 border-b border-[#DCD6D0] py-5 sm:grid-cols-[70px_1fr_150px_130px]">
                        <span class="text-xs font-bold uppercase tracking-[2px] text-[#858995]">
                            {m.leaderboard_rank()}
                        </span>

                        <span class="text-xs font-bold uppercase tracking-[2px] text-[#858995]">
                            {m.leaderboard_member()}
                        </span>

                        <span class="hidden text-xs font-bold uppercase tracking-[2px] text-[#858995] sm:block">
                            {m.leaderboard_rating()}
                        </span>

                        <span class="text-right text-xs font-bold uppercase tracking-[2px] text-[#858995]">
                            {m.leaderboard_points()}
                        </span>
                    </div>

                    <!-- ROWS -->
                    {#each remainingUsers as user, i}
                        <div class="group grid grid-cols-[50px_1fr_100px] gap-4 border-b border-[#DCD6D0] py-5 transition-colors hover:bg-[#ECE8E3] sm:grid-cols-[70px_1fr_150px_130px] sm:py-6">

                            <!-- RANK -->
                            <div class="flex items-center">
                                <span class="text-sm font-bold text-[#858995]">
                                    {String(i + 4).padStart(2, '0')}
                                </span>
                            </div>

                            <!-- USER -->
                            <div class="flex min-w-0 items-center gap-3 sm:gap-5">
                                {#if getAvatar(user)}
                                    <img
                                        src={getAvatar(user)}
                                        alt={getName(user)}
                                        class="h-12 w-12 shrink-0 rounded-full object-cover sm:h-14 sm:w-14"
                                    />
                                {:else}
                                    <div class="flex h-12 w-12 shrink-0 items-center justify-center rounded-full bg-[#A8B79E] text-sm font-black text-[#2A2E38] sm:h-14 sm:w-14">
                                        {getInitials(user)}
                                    </div>
                                {/if}

                                <div class="min-w-0">
                                    <h3 class="truncate text-sm font-bold sm:text-base">
                                        {getName(user)}
                                    </h3>

                                    {#if user.location}
                                        <p class="mt-1 flex items-center gap-1 text-xs text-[#858995]">
                                            <MapPin size={12} />
                                            <span class="truncate">{user.location}</span>
                                        </p>
                                    {/if}
                                </div>
                            </div>

                            <!-- RATING -->
                            <div class="hidden items-center sm:flex">
                                <div class="flex items-center gap-2">
                                    <Star size={16} fill="#D8AA53" stroke="#D8AA53" />

                                    <span class="text-sm font-bold">
                                        {getRating(user)}
                                    </span>

                                    <span class="text-xs text-[#858995]">
                                        ({getReviews(user)})
                                    </span>
                                </div>
                            </div>

                            <!-- SCORE -->
                            <div class="flex items-center justify-end">
                                <div class="text-right">
                                    <span class="text-lg font-black tracking-tight text-[#7C8D78]">
                                        {getScore(user)}
                                    </span>

                                    <p class="text-[10px] uppercase tracking-[1.5px] text-[#858995]">
                                        {m.leaderboard_points()}
                                    </p>
                                </div>

                                <ArrowUpRight size={18} class="ml-3 hidden text-[#858995] transition-transform group-hover:-translate-y-1 group-hover:translate-x-1 sm:block" />
                            </div>
                        </div>
                    {/each}
                </div>
            {/if}
        {/if}

        <!-- FOOTER -->
        <div class="mt-12 flex flex-col justify-between gap-4 border-t border-[#DCD6D0] pt-6 sm:flex-row sm:items-center">
            <p class="text-xs uppercase tracking-[2px] text-[#858995]">
                {m.leaderboard_footer_community()}
            </p>

            <p class="text-xs text-[#858995]">
                {m.leaderboard_footer_slogan()}
            </p>
        </div>
    </section>
</div>
