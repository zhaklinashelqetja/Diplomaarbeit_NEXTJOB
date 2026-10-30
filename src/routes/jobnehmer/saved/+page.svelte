<script>
    import { t } from '$lib/i18n.js';

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
    <title>{$t('saved_title')} | NextJob</title>
    <meta
        name="description"
        content={$t('saved_meta_description')}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-7xl px-4 py-7 sm:px-6 sm:py-10">
        <!-- SEITENKOPF -->
        <section class="mb-8">
            <p
                class="text-sm font-semibold uppercase tracking-wider text-[#398875]"
            >
                {$t('profile_my_area')}
            </p>

            <div
                class="mt-2 flex flex-wrap items-end justify-between gap-4"
            >
                <div>
                    <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">
                        {$t('saved_title')}
                    </h1>

                    <p
                        class="mt-2 max-w-2xl text-sm leading-6 text-[#2A2E38]/60 sm:text-base"
                    >
                        {$t('saved_description')}
                    </p>
                </div>

                <a
                    href="/jobnehmerHauptseite"
                    class="inline-flex items-center justify-center rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                >
                    + {$t('saved_discover_jobs')}
                </a>
            </div>
        </section>

        <!-- FEHLERMELDUNG -->
        {#if data.error}
            <div
                class="mb-6 rounded-2xl border border-[#8FB0C4]/40 bg-white p-5"
                role="alert"
            >
                <p class="font-semibold">
                    {$t('saved_title')}
                </p>

                <p class="mt-2 text-sm leading-6 text-[#2A2E38]/65">
                    {data.error}
                </p>
            </div>
        {/if}

        <!-- ANZAHL DER JOBS -->
        <section class="mb-6 flex items-center justify-between gap-3">
            <h2 class="text-sm font-semibold">
                {$t('saved_my_jobs')}
            </h2>

            <span
                class="rounded-full bg-[#A8B79E]/40 px-3 py-1.5 text-xs font-bold"
            >
                {savedJobs.length}
                {savedJobs.length === 1 ? 'Job' : 'Jobs'}
            </span>
        </section>

        <!-- JOBKARTEN -->
        {#if paginatedJobs.length > 0}
            <section class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {#each paginatedJobs as job, index (`${getJobId(job) ?? index}`)}
                    <article
                        class="flex min-w-0 flex-col rounded-2xl border border-[#2A2E38]/10 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                    >
                        <div class="flex-1 p-5">
                            <div
                                class="mb-4 flex items-start justify-between gap-3"
                            >
                                <div
                                    class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#A8B79E]/45 text-xl"
                                    aria-hidden="true"
                                >
                                    💼
                                </div>

                                {#if job.urgency === 'high' || job.urgency === 'emergency'}
                                    <span
                                        class="rounded-full bg-[#62AA97]/15 px-3 py-1 text-xs font-bold text-[#398875]"
                                    >
                                        {$t('worker_urgent')}
                                    </span>
                                {:else}
                                    <span
                                        class="rounded-full bg-[#8FB0C4]/20 px-3 py-1 text-xs font-medium"
                                    >
                                        {$t('saved_status')}
                                    </span>
                                {/if}
                            </div>

                            <h2 class="break-words text-lg font-bold">
                                {job.title ?? $t('worker_no_title')}
                            </h2>

                            <p
                                class="mt-2 line-clamp-3 break-words text-sm leading-6 text-[#2A2E38]/60"
                            >
                                {job.description ??
                                    $t('worker_no_description')}
                            </p>

                            <div class="mt-5 space-y-3">
                                {#if job.location}
                                    <p class="flex items-start gap-2 text-sm">
                                        <span aria-hidden="true">📍</span>
                                        <span
                                            class="break-words text-[#2A2E38]/70"
                                        >
                                            {job.location}
                                        </span>
                                    </p>
                                {/if}

                                {#if job.budget != null && job.budget !== ''}
                                    <p class="flex items-start gap-2 text-sm">
                                        <span aria-hidden="true">💰</span>
                                        <span class="font-semibold">
                                            {job.budget}
                                        </span>
                                    </p>
                                {/if}

                                {#if getCategory(job)}
                                    <p class="flex items-start gap-2 text-sm">
                                        <span aria-hidden="true">🏷️</span>
                                        <span
                                            class="break-words text-[#2A2E38]/70"
                                        >
                                            {getCategory(job)}
                                        </span>
                                    </p>
                                {/if}
                            </div>
                        </div>

                        <!-- AUFTRAG ANSEHEN -->
                        <div class="p-5 pt-0">
                            {#if getJobId(job) != null}
                                <a
                                    href={`/jobs/${getJobId(job)}`}
                                    class="block w-full rounded-xl bg-[#62AA97] px-4 py-3 text-center text-sm font-bold text-white transition hover:bg-[#529b88]"
                                >
                                    {$t('worker_view_job')} →
                                </a>
                            {:else}
                                <p class="text-sm text-[#2A2E38]/50">
                                    {$t('saved_no_id')}
                                </p>
                            {/if}
                        </div>
                    </article>
                {/each}
            </section>

            <!-- PAGINATION -->
            {#if totalPages > 1}
                <nav
                    class="mt-8 flex flex-wrap items-center justify-center gap-2"
                    aria-label={$t('saved_pagination')}
                >
                    <button
                        type="button"
                        onclick={() => goToPage(currentPage - 1)}
                        disabled={currentPage === 1}
                        class="rounded-xl border border-[#2A2E38]/10 bg-white px-3 py-2 text-sm font-semibold hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        ← {$t('worker_previous')}
                    </button>

                    {#each pageNumbers as page}
                        <button
                            type="button"
                            onclick={() => goToPage(page)}
                            aria-label={`${$t('worker_page')} ${page}`}
                            aria-current={currentPage === page
                                ? 'page'
                                : undefined}
                            class={`h-10 min-w-10 rounded-xl border px-3 text-sm font-semibold ${
                                currentPage === page
                                    ? 'border-[#62AA97] bg-[#62AA97] text-white'
                                    : 'border-[#2A2E38]/10 bg-white hover:border-[#62AA97]'
                            }`}
                        >
                            {page}
                        </button>
                    {/each}

                    <button
                        type="button"
                        onclick={() => goToPage(currentPage + 1)}
                        disabled={currentPage === totalPages}
                        class="rounded-xl border border-[#2A2E38]/10 bg-white px-3 py-2 text-sm font-semibold hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                    >
                        {$t('worker_next')} →
                    </button>
                </nav>

                <p class="mt-3 text-center text-xs text-[#2A2E38]/50">
                    {$t('worker_page')} {currentPage} {$t('worker_of')} {totalPages}
                </p>
            {/if}
        {:else}
            <!-- LEERZUSTAND -->
            <section
                class="rounded-2xl border border-dashed border-[#2A2E38]/15 bg-white px-5 py-14 text-center sm:px-8 sm:py-16"
            >
                <div
                    class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-[#A8B79E]/35 text-3xl"
                    aria-hidden="true"
                >
                    ♡
                </div>

                <h2 class="mt-5 text-xl font-bold">
                    {$t('saved_empty_title')}
                </h2>

                <p
                    class="mx-auto mt-2 max-w-md text-sm leading-6 text-[#2A2E38]/60"
                >
                    {$t('saved_empty_description')}
                </p>

                <a
                    href="/jobnehmerHauptseite"
                    class="mt-5 inline-block rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                >
                    {$t('saved_discover_jobs')}
                </a>
            </section>
        {/if}
    </main>
</div>