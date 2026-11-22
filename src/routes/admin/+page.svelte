
<script>
    import RegistrationGrowthChart from '$lib/components/RegistrationGrowthChart.svelte';
    import { goto } from '$app/navigation';
    import * as m from '$lib/paraglide/messages.js';

    let { data } = $props();

    const stats = $derived([
        {
            title: m.admin_stat_users(),
            value: data.stats.totalUsers,
            description: m.admin_stat_registered_users(),
            color: '#A8B79E',
            icon: '👥'
        },
        {
            title: m.admin_stat_active_jobs(),
            value: data.stats.activeJobs,
            description: m.admin_stat_current_jobs(),
            color: '#8FB0C4',
            icon: '💼'
        },
        {
            title: m.admin_stat_offers(),
            value: data.stats.totalOffers,
            description: m.admin_stat_submitted_offers(),
            color: '#62AA97',
            icon: '📋'
        },
        {
            title: m.admin_stat_reported_content(),
            value: data.stats.reportedContent,
            description: m.admin_stat_flagged_reviews(),
            color: '#D6B59C',
            icon: '⚠️'
        }
    ]);
</script>

<svelte:head>
    <title>{m.admin_page_title()} | NextJob</title>
    <meta
        name="description"
        content={m.admin_meta_description()}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-12">

        <!-- Header -->
        <section class="border-b border-[#2A2E38]/15 pb-10">
            <div class="flex flex-col justify-between gap-8 md:flex-row md:items-end">

                <div>
                    <div class="mb-5 flex items-center gap-2">
                        <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-[#2A2E38]/55">
                            {m.admin_breadcrumb()}
                        </p>
                    </div>

                    <h1 class="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
                        {m.admin_overview_title()}<span class="text-[#62AA97]">.</span>
                    </h1>

                    <p class="mt-4 max-w-xl text-sm leading-7 text-[#2A2E38]/65 sm:text-base">
                        {m.admin_overview_description()}
                    </p>
                </div>

                <div class="border-l-2 border-[#A8B79E] pl-4">
                    <p class="text-xs uppercase tracking-[0.15em] text-[#2A2E38]/45">
                        {m.admin_dashboard_label()}
                    </p>
                    <p class="mt-1 text-sm font-semibold">
                        {m.admin_management_area()}
                    </p>
                    <p class="mt-1 text-xs text-[#2A2E38]/50">
                        NextJob Admin
                    </p>
                </div>

            </div>
        </section>

        <!-- Error -->
        {#if data.error}
            <div class="mt-6 border-l-4 border-red-400 bg-red-50 px-5 py-4 text-sm text-red-700">
                {data.error}
            </div>
        {/if}

        <!-- Statistics -->
        <section class="mt-10">

            <div class="mb-7 flex flex-col gap-2 sm:flex-row sm:items-end sm:justify-between">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                        {m.admin_section_statistics()}
                    </p>

                    <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                        {m.admin_statistics_title()}
                    </h2>
                </div>

                <p class="text-xs text-[#2A2E38]/45">
                    {m.admin_current_overview()}
                </p>
            </div>

            <div class="grid grid-cols-1 gap-4 sm:grid-cols-2 xl:grid-cols-4">

                {#each stats as stat, index}
                    <article
                        class="group relative overflow-hidden border border-[#2A2E38]/10 bg-white p-5 transition duration-200 hover:border-[#62AA97]/50 sm:p-6"
                    >
                        <div class="flex items-start justify-between">

                            <div>
                                <p class="text-sm text-[#2A2E38]/60">
                                    {stat.title}
                                </p>

                                <p class="mt-5 text-4xl font-semibold tracking-tight">
                                    {stat.value}
                                </p>
                            </div>

                            <div
                                class="flex h-11 w-11 items-center justify-center text-lg"
                                style={`background-color: ${stat.color}35`}
                            >
                                {stat.icon}
                            </div>
                        </div>

                        <p class="mt-3 text-xs text-[#2A2E38]/45">
                            {stat.description}
                        </p>

                        <div
                            class="absolute bottom-0 left-0 h-1 w-full transition-all duration-300 group-hover:h-1.5"
                            style={`background-color: ${stat.color}`}
                        ></div>
                    </article>
                {/each}

            </div>
        </section>

        <!-- Administration -->
        <section class="mt-12">

            <div class="mb-6">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                    {m.admin_section_management()}
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    {m.admin_control_platform()}
                </h2>
            </div>

            <div class="relative overflow-hidden border border-[#2A2E38]/10 bg-[#E8EAE4] p-6 sm:p-8">

                <div class="flex flex-col gap-7 md:flex-row md:items-center md:justify-between">

                    <div class="max-w-xl">
                        <div class="flex items-center gap-3">
                            <div class="flex h-12 w-12 items-center justify-center bg-white text-xl">
                                ⚙️
                            </div>

                            <div>
                                <p class="text-xs uppercase tracking-[0.15em] text-[#2A2E38]/45">
                                    {m.admin_management_label()}
                                </p>

                                <h3 class="mt-1 text-xl font-semibold">
                                    {m.admin_users_jobs()}
                                </h3>
                            </div>
                        </div>

                        <p class="mt-4 text-sm leading-6 text-[#2A2E38]/65">
                            {m.admin_management_description()}
                        </p>
                    </div>

                    <button
                        type="button"
                        onclick={() => goto('/admin/verwaltung')}
                        class="flex w-full items-center justify-between gap-5 bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition duration-200 hover:bg-[#62AA97] md:w-auto"
                    >
                        {m.admin_open_management()}
                        <span class="text-lg">↗</span>
                    </button>

                </div>
            </div>
        </section>

        <!-- Platform activity -->
        <section class="mt-14">

            <div class="mb-8">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                    {m.admin_section_activity()}
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    {m.admin_activity_title()}
                </h2>

                <p class="mt-3 max-w-xl text-sm leading-6 text-[#2A2E38]/60">
                    {m.admin_activity_description()}
                </p>
            </div>

            <div class="grid gap-10 lg:grid-cols-2">

                <!-- Category demand -->
                <div class="border-t border-[#2A2E38]/15 pt-6">

                    <div class="mb-7 flex items-start justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-semibold">
                                {m.admin_category_demand()}
                            </h3>

                            <p class="mt-2 text-sm text-[#2A2E38]/55">
                                {m.admin_open_jobs_category()}
                            </p>
                        </div>

                        <span class="flex h-9 w-9 shrink-0 items-center justify-center bg-[#A8B79E]/30 text-sm">
                            01
                        </span>
                    </div>

                    {#if data.categoryDemand.length > 0}

                        <div class="space-y-7">

                            {#each data.categoryDemand.slice(0, 5) as category, index}
                                <div>

                                    <div class="mb-3 flex items-center justify-between gap-4">

                                        <div class="flex items-center gap-3">
                                            <span class="text-xs text-[#2A2E38]/40">
                                                0{index + 1}
                                            </span>

                                            <span class="text-sm font-medium">
                                                {category.name}
                                            </span>
                                        </div>

                                        <span class="text-xs text-[#2A2E38]/55">
                                            {category.open_problems} {m.admin_jobs_label()}
                                        </span>
                                    </div>

                                    <div class="h-2 w-full bg-[#2A2E38]/5">
                                        <div
                                            class="h-full bg-[#62AA97] transition-all duration-500"
                                            style={`width: ${Math.min(
                                                Number(category.open_problems || 0) * 10,
                                                100
                                            )}%`}
                                        ></div>
                                    </div>

                                </div>
                            {/each}

                        </div>

                    {:else}

                        <div class="border-b border-[#2A2E38]/10 py-8 text-sm text-[#2A2E38]/50">
                            {m.admin_no_category_data()}
                        </div>

                    {/if}

                </div>

                <!-- Top searches -->
                <div class="border-t border-[#2A2E38]/15 pt-6">

                    <div class="mb-7 flex items-start justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-semibold">
                                {m.admin_top_searches()}
                            </h3>

                            <p class="mt-2 text-sm text-[#2A2E38]/55">
                                {m.admin_search_activity()}
                            </p>
                        </div>

                        <span class="flex h-9 w-9 shrink-0 items-center justify-center bg-[#8FB0C4]/30 text-sm">
                            02
                        </span>
                    </div>

                    {#if data.topSearches.length > 0}

                        <div>

                            {#each data.topSearches.slice(0, 5) as search, index}
                                <div class="flex items-center justify-between gap-4 border-b border-[#2A2E38]/10 py-4">

                                    <div class="flex min-w-0 items-center gap-4">
                                        <span class="text-xs text-[#62AA97]">
                                            0{index + 1}
                                        </span>

                                        <span class="truncate text-sm font-medium">
                                            {search.keyword}
                                        </span>
                                    </div>

                                    <span class="shrink-0 text-sm text-[#2A2E38]/50">
                                        {search.search_count}
                                        <span class="text-xs">
                                            {m.admin_requests_label()}
                                        </span>
                                    </span>

                                </div>
                            {/each}

                        </div>

                    {:else}

                        <div class="border-b border-[#2A2E38]/10 py-8 text-sm text-[#2A2E38]/50">
                            {m.admin_no_search_data()}
                        </div>

                    {/if}

                </div>

            </div>
        </section>

        <!-- Growth -->
        <section class="mt-14">

            <div class="mb-8">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                    {m.admin_section_growth()}
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    {m.admin_user_growth()}
                </h2>

                <p class="mt-3 max-w-xl text-sm leading-6 text-[#2A2E38]/60">
                    {m.admin_growth_description()}
                </p>
            </div>

            <div class="border border-[#2A2E38]/10 bg-white p-4 sm:p-7">
                <RegistrationGrowthChart data={data.registrationGrowth} />
            </div>

        </section>

        <!-- Footer -->
        <footer class="mt-14 border-t border-[#2A2E38]/15 py-6">

            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">

                <div>
                    <span class="text-sm font-semibold tracking-wide">
                        NEXTJOB
                    </span>

                    <span class="ml-2 text-xs text-[#2A2E38]/45">
                        {m.admin_footer_area()}
                    </span>
                </div>

                <p class="text-xs text-[#2A2E38]/45">
                    {m.admin_footer_management()}
                </p>

            </div>

        </footer>

    </main>
</div>
