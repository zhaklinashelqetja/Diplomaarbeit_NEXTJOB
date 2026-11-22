
<script>
    import { t } from '$lib/i18n.js';
    import {
        Search,
        X,
        ArrowUpRight,
        ArrowRight,
        ArrowLeft,
        MapPin,
        BriefcaseBusiness,
        Euro,
        Tag,
        Star,
        Bookmark,
        Sparkles
    } from '@lucide/svelte';

    let { data } = $props();

    let selectedCategory = $state('Alle');
    let search = $state('');
    let currentPage = $state(1);

    const categories = [
        'Alle',
        'Plumber',
        'Electrician',
        'Painter',
        'Carpenter',
        'Mason',
        'Roofer',
        'Gardener',
        'Cleaner'
    ];

    const pageSize = $derived(data.pageSize ?? 6);

    function getCategory(job) {
        if (typeof job.category === 'string') {
            return job.category;
        }

        return job.category?.name ?? job.category_name ?? '';
    }

    function normalizeText(value) {
        return String(value ?? '')
            .toLocaleLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim();
    }

    function getSearchableText(job) {
        return normalizeText(
            [
                job.title,
                job.description,
                job.location,
                getCategory(job)
            ]
                .filter(Boolean)
                .join(' ')
        );
    }

    function getWords(text) {
        return normalizeText(text)
            .split(/[\s,.;:!?/\\()[\]{}_-]+/)
            .filter(Boolean);
    }

    function editDistance(first, second) {
        if (first === second) return 0;
        if (!first.length) return second.length;
        if (!second.length) return first.length;

        const rows = first.length + 1;
        const columns = second.length + 1;

        const matrix = Array.from(
            { length: rows },
            () => Array(columns).fill(0)
        );

        for (let i = 0; i < rows; i++) {
            matrix[i][0] = i;
        }

        for (let j = 0; j < columns; j++) {
            matrix[0][j] = j;
        }

        for (let i = 1; i < rows; i++) {
            for (let j = 1; j < columns; j++) {
                const cost =
                    first[i - 1] === second[j - 1] ? 0 : 1;

                matrix[i][j] = Math.min(
                    matrix[i - 1][j] + 1,
                    matrix[i][j - 1] + 1,
                    matrix[i - 1][j - 1] + cost
                );

                if (
                    i > 1 &&
                    j > 1 &&
                    first[i - 1] === second[j - 2] &&
                    first[i - 2] === second[j - 1]
                ) {
                    matrix[i][j] = Math.min(
                        matrix[i][j],
                        matrix[i - 2][j - 2] + 1
                    );
                }
            }
        }

        return matrix[first.length][second.length];
    }

    function wordMatches(term, word) {
        if (word.includes(term) || term.includes(word)) {
            return true;
        }

        if (term.length < 4 || word.length < 4) {
            return false;
        }

        const maxDistance = term.length >= 8 ? 2 : 1;

        if (Math.abs(term.length - word.length) > maxDistance) {
            return false;
        }

        return editDistance(term, word) <= maxDistance;
    }

    function matchesSearch(job, searchText) {
        const terms = getWords(searchText);

        if (terms.length === 0) {
            return true;
        }

        const searchableText = getSearchableText(job);
        const words = getWords(searchableText);

        return terms.every((term) =>
            words.some((word) => wordMatches(term, word))
        );
    }

    let filteredJobs = $derived(
        (data.jobs ?? []).filter((job) => {
            const matchesText = matchesSearch(job, search);

            const category = normalizeText(getCategory(job));
            const selected = normalizeText(selectedCategory);

            const matchesCategory =
                selectedCategory === 'Alle' ||
                category === selected;

            return matchesText && matchesCategory;
        })
    );

    let totalPages = $derived(
        Math.max(1, Math.ceil(filteredJobs.length / pageSize))
    );

    let paginatedJobs = $derived(
        filteredJobs.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
        )
    );

    let pageNumbers = $derived(
        Array.from({ length: totalPages }, (_, index) => index + 1)
    );

    function updateSearch(value) {
        search = value;
        currentPage = 1;
    }

    function updateCategory(category) {
        selectedCategory = category;
        currentPage = 1;
    }

    function goToPage(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
        }
    }

    function resetFilters() {
        search = '';
        selectedCategory = 'Alle';
        currentPage = 1;
    }
</script>

<svelte:head>
    <title>{$t('worker_page_title')} | NextJob</title>
    <meta
        name="description"
        content={$t('worker_meta_description')}
    />
</svelte:head>

<div class="min-h-screen overflow-hidden bg-[#F5F1EE] px-4 py-6 text-[#2A2E38] sm:px-6 sm:py-8 lg:px-12 xl:px-20">

    <!-- HERO -->
    <section class="mx-auto mb-16 grid max-w-7xl grid-cols-1 gap-5 lg:grid-cols-[1.65fr_0.75fr]">

        <!-- HERO COPY -->
        <div class="flex min-h-[330px] flex-col justify-between border border-[#2A2E38]/10 bg-white/60 p-7 sm:p-10 lg:min-h-[400px] lg:p-14">

            <p class="flex items-center gap-2 text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                {$t('worker_for_you')}
            </p>

            <div class="my-10">
                <h1 class="max-w-4xl break-words text-5xl font-medium leading-[0.98] tracking-[-0.06em] sm:text-6xl lg:text-8xl">
                    {$t('worker_welcome')}
                    <span class="text-[#398875]">
                        {data.user?.first_name ?? ''}
                    </span><span class="text-[#62AA97]">.</span>
                </h1>

                <p class="mt-6 max-w-2xl text-sm leading-7 text-[#2A2E38]/60 sm:text-base sm:leading-8">
                    {$t('worker_intro')}
                </p>
            </div>

            <div class="flex items-center justify-between gap-4 border-t border-[#2A2E38]/10 pt-5">
                <p class="flex items-center gap-2 text-sm">
                    <MapPin size={17} strokeWidth={1.5} />
                    Shkodër
                </p>

                <span class="text-[10px] tracking-[0.15em] text-[#2A2E38]/40 sm:text-xs">
                    01 — NEXTJOB
                </span>
            </div>
        </div>

        <!-- DARK HERO PANEL -->
        <div class="flex min-h-[260px] flex-col justify-between bg-[#2A2E38] p-7 text-white sm:p-9 lg:min-h-[400px]">

            <div class="flex items-center justify-between">
                <span class="text-xs tracking-[0.15em] text-[#A8B79E]">01</span>
                <ArrowUpRight size={36} strokeWidth={1.2} />
            </div>

            <div class="my-8">
                <p class="mb-3 text-xs uppercase tracking-[0.15em] text-white/50">
                    {$t('worker_matching_jobs')}
                </p>

                <div class="flex items-end gap-4">
                    <span class="text-7xl font-normal leading-none tracking-[-0.07em] text-[#A8B79E] sm:text-8xl">
                        {filteredJobs.length}
                    </span>

                    <span class="mb-2 text-sm text-white/60">
                        {filteredJobs.length === 1 ? 'Job' : 'Jobs'}
                    </span>
                </div>
            </div>

            <div class="flex items-center gap-2 border-t border-white/15 pt-5 text-xs text-white/60">
                <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                {$t('worker_recommendations')}
            </div>
        </div>
    </section>

    <!-- ERROR -->
    {#if data.error}
        <div class="mx-auto mb-8 max-w-7xl border border-[#8FB0C4]/50 bg-[#8FB0C4]/20 p-5" role="status">
            <p class="font-medium">{data.error}</p>
        </div>
    {/if}

    <!-- SEARCH -->
    <section class="mx-auto mb-16 max-w-7xl">

        <div class="flex flex-wrap items-end justify-between gap-5">
            <div>
                <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                    02 — {$t('worker_search')}
                </p>

                <h2 class="mt-4 text-3xl font-medium tracking-[-0.045em] sm:text-5xl">
                    {$t('worker_matching_jobs')}
                </h2>
            </div>

            <span class="border border-[#2A2E38]/10 bg-[#A8B79E]/25 px-4 py-2 text-sm">
                {filteredJobs.length} {filteredJobs.length === 1 ? 'Job' : 'Jobs'}
            </span>
        </div>

        <!-- SEARCH FIELD -->
        <div class="mt-8 flex items-center gap-4 border border-[#2A2E38]/10 bg-white/70 px-5 py-4 transition focus-within:border-[#62AA97]">

            <Search size={21} strokeWidth={1.5} class="shrink-0 text-[#2A2E38]/40" />

            <input
                id="job-search"
                type="search"
                value={search}
                oninput={(event) => updateSearch(event.currentTarget.value)}
                placeholder={$t('worker_search_placeholder')}
                autocomplete="off"
                class="w-full min-w-0 border-none bg-transparent text-[#2A2E38] outline-none placeholder:text-[#2A2E38]/40"
            />

            {#if search}
                <button
                    type="button"
                    onclick={() => updateSearch('')}
                    aria-label={$t('worker_clear_search')}
                    class="flex shrink-0 items-center justify-center text-[#2A2E38]/50 transition hover:text-[#2A2E38]"
                >
                    <X size={19} />
                </button>
            {/if}
        </div>

        <p class="mt-3 text-xs leading-6 text-[#2A2E38]/50">
            {$t('worker_search_hint')}
        </p>

        <!-- CATEGORIES -->
        <div class="mt-8 border-t border-[#2A2E38]/10 pt-6">

            <div class="mb-5 flex items-center justify-between gap-3">
                <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                    {$t('worker_page_title')}
                </p>

                <span class="text-xs text-[#2A2E38]/40">
                    {categories.length} categories
                </span>
            </div>

            <div class="flex flex-nowrap gap-2 overflow-x-auto pb-3 scrollbar-thin">
                {#each categories as category}
                    <button
                        type="button"
                        onclick={() => updateCategory(category)}
                        aria-pressed={selectedCategory === category}
                        class={`shrink-0 border px-4 py-3 text-sm transition duration-200 ${
                            selectedCategory === category
                                ? 'border-[#2A2E38] bg-[#2A2E38] text-white'
                                : 'border-[#2A2E38]/10 bg-transparent text-[#2A2E38] hover:border-[#62AA97]'
                        }`}
                    >
                        {$t(`worker_category_${category === 'Alle' ? 'all' : category}`)}
                    </button>
                {/each}
            </div>
        </div>
    </section>

    <!-- JOBS + SIDEBAR -->
    <section class="mx-auto grid max-w-7xl grid-cols-1 items-start gap-8 lg:grid-cols-[minmax(0,1fr)_290px] lg:gap-10">

        <!-- JOB LIST -->
        <div class="min-w-0">

            <div class="mb-8 flex flex-wrap items-end justify-between gap-5">

                <div>
                    <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                        03 — NEXTJOB
                    </p>

                    <h2 class="mt-4 text-3xl font-medium tracking-[-0.045em] sm:text-5xl">
                        {$t('worker_matching_jobs')}
                    </h2>

                    <p class="mt-3 text-sm leading-7 text-[#2A2E38]/50">
                        {$t('worker_recommendations')}
                    </p>
                </div>

                <div class="flex items-center gap-3 pb-1">
                    <span class="text-4xl font-medium tracking-[-0.05em]">
                        {filteredJobs.length}
                    </span>

                    <span class="text-xs text-[#2A2E38]/50">
                        {filteredJobs.length === 1 ? 'Job' : 'Jobs'}
                    </span>
                </div>
            </div>

            {#if paginatedJobs.length > 0}

                <!-- JOB CARDS -->
                <div class="grid grid-cols-1 gap-5 sm:grid-cols-2">

                    {#each paginatedJobs as job, index (`${job.problem_id ?? job.id ?? index}`)}

                        <article class="flex min-w-0 flex-col border border-[#2A2E38]/10 bg-white/60 p-6 transition duration-300 hover:-translate-y-1 hover:border-[#62AA97]/50 hover:bg-white">

                            <!-- CARD TOP -->
                            <div class="mb-6 flex items-start justify-between gap-3">

                                <div class="flex h-12 w-12 shrink-0 items-center justify-center bg-[#A8B79E]/30 text-[#2A2E38]">
                                    <BriefcaseBusiness size={24} strokeWidth={1.4} />
                                </div>

                                {#if job.urgency === 'high' || job.urgency === 'emergency'}
                                    <span class="flex items-center gap-2 bg-[#62AA97]/15 px-3 py-2 text-xs font-semibold text-[#398875]">
                                        <span class="h-1.5 w-1.5 rounded-full bg-[#62AA97]"></span>
                                        {$t('worker_urgent')}
                                    </span>
                                {:else}
                                    <span class="flex items-center gap-2 bg-[#8FB0C4]/20 px-3 py-2 text-xs font-medium text-[#2A2E38]">
                                        <span class="h-1.5 w-1.5 rounded-full bg-[#8FB0C4]"></span>
                                        {$t('worker_open')}
                                    </span>
                                {/if}
                            </div>

                            <!-- REFERENCE -->
                            <p class="mb-3 text-[10px] tracking-[0.15em] text-[#2A2E38]/40">
                                JOB — {String(index + 1).padStart(2, '0')}
                            </p>

                            <!-- TITLE -->
                            <h3 class="break-words text-2xl font-medium leading-snug tracking-[-0.04em]">
                                {job.title ?? $t('worker_no_title')}
                            </h3>

                            <!-- DESCRIPTION -->
                            <p class="mt-4 line-clamp-4 break-words text-sm leading-7 text-[#2A2E38]/60">
                                {job.description ?? $t('worker_no_description')}
                            </p>

                            <!-- DETAILS -->
                            <div class="mt-6 flex flex-col gap-4 border-t border-[#2A2E38]/10 pt-5">

                                {#if job.location}
                                    <div class="flex items-start gap-3 text-sm">
                                        <MapPin size={17} strokeWidth={1.5} class="shrink-0 text-[#398875]" />
                                        <span class="break-words">{job.location}</span>
                                    </div>
                                {/if}

                                {#if job.budget != null && job.budget !== ''}
                                    <div class="flex items-start gap-3 text-sm">
                                        <Euro size={17} strokeWidth={1.5} class="shrink-0 text-[#398875]" />
                                        <span class="break-words">{job.budget}</span>
                                    </div>
                                {/if}

                                {#if getCategory(job)}
                                    <div class="flex items-start gap-3 text-sm">
                                        <Tag size={17} strokeWidth={1.5} class="shrink-0 text-[#398875]" />
                                        <span class="break-words">{getCategory(job)}</span>
                                    </div>
                                {/if}
                            </div>

                            <!-- CTA -->
                            <div class="mt-6 border-t border-[#2A2E38]/10 pt-5">
                                <a
                                    href={`/jobs/${job.problem_id ?? job.id}`}
                                    class="flex items-center justify-between gap-3 text-sm font-semibold text-[#2A2E38] transition hover:text-[#398875]"
                                >
                                    {$t('worker_view_job')}
                                    <ArrowUpRight size={20} strokeWidth={1.5} />
                                </a>
                            </div>

                        </article>
                    {/each}
                </div>

                <!-- PAGINATION -->
                {#if totalPages > 1}
                    <nav
                        class="mt-10 flex flex-wrap items-center justify-center gap-2"
                        aria-label={$t('worker_pagination')}
                    >

                        <button
                            type="button"
                            onclick={() => goToPage(currentPage - 1)}
                            disabled={currentPage === 1}
                            class="flex items-center gap-2 border border-[#2A2E38]/10 px-4 py-3 text-sm transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-30"
                        >
                            <ArrowLeft size={18} />
                            {$t('worker_previous')}
                        </button>

                        <div class="flex flex-wrap gap-2">
                            {#each pageNumbers as page}
                                <button
                                    type="button"
                                    onclick={() => goToPage(page)}
                                    aria-label={`${$t('worker_page')} ${page}`}
                                    aria-current={currentPage === page ? 'page' : undefined}
                                    class={`min-h-10 min-w-10 border px-3 text-sm transition ${
                                        currentPage === page
                                            ? 'border-[#2A2E38] bg-[#2A2E38] text-white'
                                            : 'border-[#2A2E38]/10 bg-transparent hover:border-[#62AA97]'
                                    }`}
                                >
                                    {page}
                                </button>
                            {/each}
                        </div>

                        <button
                            type="button"
                            onclick={() => goToPage(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            class="flex items-center gap-2 border border-[#2A2E38]/10 px-4 py-3 text-sm transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-30"
                        >
                            {$t('worker_next')}
                            <ArrowRight size={18} />
                        </button>
                    </nav>

                    <p class="mt-4 text-center text-xs text-[#2A2E38]/50">
                        {$t('worker_page')} {currentPage} {$t('worker_of')} {totalPages}
                    </p>
                {/if}

            {:else}

                <!-- EMPTY STATE -->
                <div class="border border-dashed border-[#2A2E38]/20 bg-white/50 px-6 py-14 text-center sm:py-20">

                    <div class="mx-auto mb-6 flex h-20 w-20 items-center justify-center rounded-full bg-[#A8B79E]/25">
                        <Search size={36} strokeWidth={1.3} />
                    </div>

                    <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                        NEXTJOB — 03
                    </p>

                    <h3 class="mt-5 text-2xl font-medium tracking-[-0.04em]">
                        {search.trim() || selectedCategory !== 'Alle'
                            ? $t('worker_no_results')
                            : $t('worker_no_jobs')}
                    </h3>

                    <p class="mx-auto mt-3 max-w-md text-sm leading-7 text-[#2A2E38]/50">
                        {search.trim() || selectedCategory !== 'Alle'
                            ? $t('worker_try_again')
                            : $t('worker_check_later')}
                    </p>

                    {#if search.trim() || selectedCategory !== 'Alle'}
                        <button
                            type="button"
                            onclick={resetFilters}
                            class="mt-6 inline-flex items-center gap-3 bg-[#62AA97] px-5 py-3 text-sm font-semibold text-white transition hover:bg-[#398875]"
                        >
                            {$t('worker_reset')}
                            <ArrowRight size={18} />
                        </button>
                    {/if}
                </div>
            {/if}
        </div>

        <!-- SIDEBAR -->
        <aside class="flex flex-col gap-5">

            <!-- PROFILE -->
            <section class="bg-[#2A2E38] p-6 text-white sm:p-7">

                <div class="flex items-center justify-between gap-3">
                    <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#A8B79E]">
                        04 — {$t('worker_role')}
                    </p>

                    <ArrowUpRight size={23} strokeWidth={1.4} />
                </div>

                <div class="mt-8 flex h-16 w-16 items-center justify-center rounded-full bg-[#A8B79E] text-2xl font-medium text-[#2A2E38]">
                    {data.user?.first_name?.charAt(0) ?? 'U'}
                </div>

                <h3 class="mt-5 break-words text-2xl font-medium tracking-[-0.04em]">
                    {data.user?.first_name ?? ''}
                    {data.user?.last_name ?? ''}
                </h3>

                <p class="mt-2 text-sm text-white/50">
                    {$t('worker_role')}
                </p>

                <a
                    href="/jobnehmer/profil"
                    class="mt-6 flex items-center justify-between gap-3 bg-[#A8B79E] px-4 py-4 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#c0cbb8]"
                >
                    {$t('worker_view_profile')}
                    <ArrowRight size={18} />
                </a>
            </section>

            <!-- SAVED JOBS -->
            <section class="border border-[#2A2E38]/10 bg-white/60 p-6">

                <div class="flex items-start gap-4">
                    <div class="flex h-11 w-11 shrink-0 items-center justify-center bg-[#A8B79E]/30">
                        <Bookmark size={21} strokeWidth={1.5} />
                    </div>

                    <div>
                        <h3 class="font-semibold">
                            {$t('worker_saved_jobs')}
                        </h3>

                        <p class="mt-2 text-xs leading-5 text-[#2A2E38]/50">
                            {$t('worker_saved_description')}
                        </p>
                    </div>
                </div>

                <div class="mt-6 flex items-end gap-3">
                    <span class="text-4xl font-medium tracking-[-0.05em]">
                        {data.savedJobs?.length ?? 0}
                    </span>

                    <span class="mb-1 text-xs text-[#2A2E38]/50">
                        {$t('worker_saved_jobs')}
                    </span>
                </div>

                <a
                    href="/jobnehmer/saved"
                    class="mt-5 flex items-center justify-between gap-3 border-t border-[#2A2E38]/10 pt-5 text-sm font-semibold text-[#398875] transition hover:text-[#2A2E38]"
                >
                    {$t('worker_saved_jobs')}
                    <ArrowUpRight size={19} />
                </a>
            </section>

        </aside>
    </section>

    <!-- FOOTER VISUAL -->
    <section class="mx-auto mt-20 flex max-w-7xl items-center justify-between gap-6 border-y border-[#2A2E38]/15 py-10">

        <div>
            <p class="text-xs font-bold uppercase tracking-[0.15em] text-[#398875]">
                NEXTJOB — SHKODËR
            </p>

            <h2 class="mt-5 text-4xl font-medium leading-tight tracking-[-0.06em] sm:text-5xl lg:text-6xl">
                Local skills.<br />
                Local opportunities.
            </h2>
        </div>

        <ArrowUpRight
            size={55}
            strokeWidth={1.2}
            class="shrink-0 text-[#398875]"
        />
    </section>

</div>
