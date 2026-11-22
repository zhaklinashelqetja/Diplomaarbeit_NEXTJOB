
<script>
    import * as m from '$lib/paraglide/messages.js';

    let { data } = $props();

    let currentPage = $state(1);

    const pageSize = 6;

    function getCategory(job) {
        if (typeof job.category === 'string') {
            return job.category;
        }

        return job.category?.name ?? job.category_name ?? '';
    }

    function getJobId(job) {
        return job.problem_id ?? job.job_id ?? job.id;
    }

    let savedJobs = $derived(data.savedJobs ?? []);

    let totalPages = $derived(
        Math.max(1, Math.ceil(savedJobs.length / pageSize))
    );

    let paginatedJobs = $derived(
        savedJobs.slice(
            (currentPage - 1) * pageSize,
            currentPage * pageSize
        )
    );

    let pageNumbers = $derived(
        Array.from({ length: totalPages }, (_, index) => index + 1)
    );

    function goToPage(page) {
        if (page >= 1 && page <= totalPages) {
            currentPage = page;
        }
    }
</script>

<svelte:head>
    <title>{m.saved_title()} | NextJob</title>
    <meta
        name="description"
        content={m.saved_meta_description()}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-10">

        <!-- HEADER -->
        <section class="mb-12">
            <div class="flex flex-col justify-between gap-6 sm:flex-row sm:items-end">
                <div>
                    <p class="text-xs font-semibold uppercase tracking-[0.22em] text-[#398875]">
                        NEXTJOB / {m.profile_my_area()}
                    </p>

                    <h1 class="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">
                        {m.saved_title()}
                    </h1>

                    <p class="mt-4 max-w-xl text-sm leading-7 text-[#2A2E38]/60 sm:text-base">
                        {m.saved_description()}
                    </p>
                </div>

            </div>
        </section>

        <!-- ERROR -->
        {#if data.error}
            <section
                class="mb-8 border-l-4 border-[#62AA97] bg-white p-6"
                role="alert"
            >
                <h2 class="font-semibold">
                    {m.saved_title()}
                </h2>

                <p class="mt-2 text-sm leading-7 text-[#2A2E38]/60">
                    {data.error}
                </p>
            </section>
        {/if}

        <!-- JOB OVERVIEW -->
        <section class="mb-7">
            <div class="flex flex-wrap items-end justify-between gap-4 border-b border-[#2A2E38]/15 pb-5">
                <div>
                    <p class="text-xs uppercase tracking-[0.18em] text-[#2A2E38]/45">
                        NEXTJOB / {m.saved_collection()}
                    </p>

                    <h2 class="mt-2 text-xl font-semibold tracking-tight sm:text-2xl">
                        {m.saved_my_jobs()}
                    </h2>
                </div>

                <div class="flex items-center gap-3">
                    <span class="text-sm text-[#2A2E38]/50">
                        {m.saved_title()}
                    </span>

                    <span class="flex h-10 min-w-10 items-center justify-center border border-[#62AA97] bg-[#A8B79E]/30 px-3 text-sm font-semibold">
                        {savedJobs.length}
                    </span>
                </div>
            </div>
        </section>

        <!-- JOB CARDS -->
        {#if paginatedJobs.length > 0}

            <section class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {#each paginatedJobs as job, index (`${getJobId(job) ?? index}`)}
                    <article
                        class="group flex min-w-0 flex-col border border-[#2A2E38]/10 bg-white transition duration-300 hover:border-[#62AA97] hover:-translate-y-1"
                    >
                        <!-- CARD CONTENT -->
                        <div class="flex-1 p-6">

                            <!-- TOP -->
                            <div class="flex items-center justify-between gap-3">
                                <div class="flex h-12 w-12 items-center justify-center bg-[#A8B79E]/30 text-xl text-[#2A2E38] transition group-hover:bg-[#A8B79E]/60">
                                    <span aria-hidden="true">↗</span>
                                </div>

                                {#if job.urgency === 'high' || job.urgency === 'emergency'}
                                    <span class="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-[#398875]">
                                        <span class="h-2 w-2 rounded-full bg-[#62AA97]"></span>
                                        {m.worker_urgent()}
                                    </span>
                                {:else}
                                    <span class="text-xs font-medium text-[#2A2E38]/50">
                                        {m.saved_status()}
                                    </span>
                                {/if}
                            </div>

                            <!-- TITLE -->
                            <h2 class="mt-6 break-words text-xl font-semibold leading-snug tracking-tight transition group-hover:text-[#398875]">
                                {job.title ?? m.worker_no_title()}
                            </h2>

                            <!-- DESCRIPTION -->
                            <p class="mt-3 line-clamp-3 break-words text-sm leading-7 text-[#2A2E38]/60">
                                {job.description ??
                                    m.worker_no_description()}
                            </p>

                            <!-- DETAILS -->
                            <div class="mt-6 space-y-4 border-t border-[#2A2E38]/10 pt-5">

                                {#if getCategory(job)}
                                    <div class="flex items-start gap-3">
                                        <span class="text-sm text-[#398875]" aria-hidden="true">
                                            ◈
                                        </span>

                                        <div class="min-w-0">
                                            <p class="text-[10px] font-medium uppercase tracking-[0.15em] text-[#2A2E38]/40">
                                                {m.worker_category()}
                                            </p>

                                            <p class="mt-1 break-words text-sm font-medium">
                                                {getCategory(job)}
                                            </p>
                                        </div>
                                    </div>
                                {/if}

                                {#if job.location}
                                    <div class="flex items-start gap-3">
                                        <span class="text-sm text-[#398875]" aria-hidden="true">
                                            ⌖
                                        </span>

                                        <div class="min-w-0">
                                            <p class="text-[10px] font-medium uppercase tracking-[0.15em] text-[#2A2E38]/40">
                                                {m.profile_location()}
                                            </p>

                                            <p class="mt-1 break-words text-sm font-medium">
                                                {job.location}
                                            </p>
                                        </div>
                                    </div>
                                {/if}

                                {#if job.budget != null && job.budget !== ''}
                                    <div class="flex items-start gap-3">
                                        <span class="text-sm text-[#398875]" aria-hidden="true">
                                            €
                                        </span>

                                        <div class="min-w-0">
                                            <p class="text-[10px] font-medium uppercase tracking-[0.15em] text-[#2A2E38]/40">
                                                {m.saved_budget()}
                                            </p>

                                            <p class="mt-1 break-words text-sm font-semibold">
                                                {job.budget}
                                            </p>
                                        </div>
                                    </div>
                                {/if}
                            </div>
                        </div>

                        <!-- CARD FOOTER -->
                        <div class="border-t border-[#2A2E38]/10 p-6 pt-4">
                            {#if getJobId(job) != null}
                                <a
                                    href={`/jobs/${getJobId(job)}`}
                                    class="group/link flex w-full items-center justify-between bg-[#A8B79E] px-4 py-3 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#62AA97]"
                                >
                                    <span>{m.worker_view_job()}</span>

                                    <span class="transition group-hover/link:translate-x-1">
                                        →
                                    </span>
                                </a>
                            {:else}
                                <p class="text-sm text-[#2A2E38]/50">
                                    {m.saved_no_id()}
                                </p>
                            {/if}
                        </div>
                    </article>
                {/each}
            </section>

            <!-- PAGINATION -->
            {#if totalPages > 1}
                <nav
                    class="mt-12 border-t border-[#2A2E38]/10 pt-6"
                    aria-label={m.saved_pagination()}
                >
                    <div class="flex flex-wrap items-center justify-center gap-2">

                        <!-- PREVIOUS -->
                        <button
                            type="button"
                            onclick={() => goToPage(currentPage - 1)}
                            disabled={currentPage === 1}
                            class="flex items-center gap-2 border border-[#2A2E38]/10 bg-white px-4 py-3 text-sm font-medium transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            <span>←</span>
                            {m.worker_previous()}
                        </button>

                        <!-- PAGE NUMBERS -->
                        {#each pageNumbers as page}
                            <button
                                type="button"
                                onclick={() => goToPage(page)}
                                aria-label={`${m.worker_page()} ${page}`}
                                aria-current={currentPage === page
                                    ? 'page'
                                    : undefined}
                                class={`flex h-11 min-w-11 items-center justify-center border px-3 text-sm font-semibold transition ${
                                    currentPage === page
                                        ? 'border-[#2A2E38] bg-[#2A2E38] text-white'
                                        : 'border-[#2A2E38]/10 bg-white hover:border-[#62AA97]'
                                }`}
                            >
                                {page}
                            </button>
                        {/each}

                        <!-- NEXT -->
                        <button
                            type="button"
                            onclick={() => goToPage(currentPage + 1)}
                            disabled={currentPage === totalPages}
                            class="flex items-center gap-2 border border-[#2A2E38]/10 bg-white px-4 py-3 text-sm font-medium transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                        >
                            {m.worker_next()}
                            <span>→</span>
                        </button>
                    </div>

                    <p class="mt-5 text-center text-xs tracking-wide text-[#2A2E38]/45">
                        {m.worker_page()} {currentPage} {m.worker_of()} {totalPages}
                    </p>
                </nav>
            {/if}

        {:else}

            <!-- EMPTY STATE -->
            <section class="relative overflow-hidden border border-[#2A2E38]/10 bg-white">

                <div class="grid md:grid-cols-[1fr_280px]">

                    <!-- TEXT -->
                    <div class="flex flex-col justify-center px-6 py-12 sm:px-10 sm:py-16 lg:px-14">
                        <p class="text-xs font-semibold uppercase tracking-[0.2em] text-[#398875]">
                            NEXTJOB / 00
                        </p>

                        <h2 class="mt-5 max-w-lg text-3xl font-semibold tracking-tight sm:text-4xl">
                            {m.saved_empty_title()}
                        </h2>

                        <p class="mt-5 max-w-lg text-sm leading-8 text-[#2A2E38]/60 sm:text-base">
                            {m.saved_empty_description()}
                        </p>

                    </div>

                    <!-- VISUAL -->
                    <div class="flex min-h-[220px] items-center justify-center border-t border-[#2A2E38]/10 bg-[#A8B79E]/25 px-6 py-10 md:border-t-0 md:border-l">
                        <div class="relative flex h-40 w-40 items-center justify-center">
                            <div class="absolute inset-0 border border-[#2A2E38]/15"></div>

                            <div class="absolute inset-5 border border-[#2A2E38]/15"></div>

                            <span class="relative text-7xl font-light text-[#2A2E38]/50">
                                ♡
                            </span>
                        </div>
                    </div>
                </div>

                <div class="border-t border-[#2A2E38]/10 px-6 py-4 sm:px-10">
                    <p class="text-[10px] uppercase tracking-[0.2em] text-[#2A2E38]/40">
                        NEXTJOB / {m.saved_footer_tagline()}
                    </p>
                </div>
            </section>

        {/if}
    </main>
</div>
