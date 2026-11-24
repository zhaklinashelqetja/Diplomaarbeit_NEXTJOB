
<script>
    import { onMount } from 'svelte';
    import { page } from '$app/state';
    import { goto } from '$app/navigation';
    import { resolve } from '$app/paths';
    import { API_URL, localizedUrl } from '$lib/api.js';
    import * as m from '$lib/paraglide/messages.js';

    import {
        Search,
        BriefcaseBusiness,
        UserRound,
        MapPin,
        ArrowUpRight,
        AlertCircle,
        LoaderCircle,
        MessageCircle
    } from '@lucide/svelte';

    let problems = $state([]);
    let workers = $state([]);
    let loading = $state(true);
    let error = $state('');

    let query = $derived(page.url.searchParams.get('q') ?? '');
    let category = $derived(page.url.searchParams.get('type') ?? 'all');

    let searchInput = $state('');
    let selectedCategory = $state('all');

    let initialized = $state(false);

    const normalize = (value) =>
        String(value ?? '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .toLocaleLowerCase()
            .trim();

    function matches(value, term) {
        return normalize(value).includes(normalize(term));
    }

    let filteredProblems = $derived(
        problems.filter((job) =>
            matches(
                [
                    (job.title_localized ?? job.title),
                    (job.category_localized ?? job.category),
                    job.neighborhood
                ].join(' '),
                query
            )
        )
    );

    let filteredWorkers = $derived(
        workers.filter((worker) =>
            matches(
                [
                    worker.full_name,
                    (worker.headline_localized ?? worker.headline),
                    worker.neighborhood
                ].join(' '),
                query
            )
        )
    );

    let visibleProblems = $derived(
        category === 'users' ? [] : filteredProblems
    );

    let visibleWorkers = $derived(
        category === 'jobs' ? [] : filteredWorkers
    );

    let totalResults = $derived(
        visibleProblems.length + visibleWorkers.length
    );

    function submitSearch(event) {
        event.preventDefault();

        const params = new URLSearchParams();

        if (searchInput.trim()) {
            params.set('q', searchInput.trim());
        }

        params.set('type', selectedCategory);

        goto(`${resolve('/suche')}?${params.toString()}`);
    }

    function changeCategory(value) {
        selectedCategory = value;

        const params = new URLSearchParams();

        if (query.trim()) {
            params.set('q', query.trim());
        }

        params.set('type', value);

        goto(`${resolve('/suche')}?${params.toString()}`);
    }

    $effect(() => {
        searchInput = query;
        selectedCategory = ['all', 'jobs', 'users'].includes(category)
            ? category
            : 'all';
    });

    onMount(() => {
        initialized = true;

        const controller = new AbortController();

        async function loadResults() {
            loading = true;
            error = '';

            try {
                const responses = await Promise.allSettled([
                    fetch(localizedUrl(`${API_URL}/api/problems`), {
                        signal: controller.signal
                    }),
                    fetch(localizedUrl(`${API_URL}/api/workers`), {
                        signal: controller.signal
                    })
                ]);

                const failed = [];

                if (
                    responses[0].status === 'fulfilled' &&
                    responses[0].value.ok
                ) {
                    const data = await responses[0].value.json();
                    problems = Array.isArray(data) ? data : [];
                } else {
                    failed.push(m.search_jobs());
                }

                if (
                    responses[1].status === 'fulfilled' &&
                    responses[1].value.ok
                ) {
                    const data = await responses[1].value.json();
                    workers = Array.isArray(data) ? data : [];
                } else {
                    failed.push(m.search_workers());
                }

                if (failed.length) {
                    error = m.search_load_failed({
                        items: failed.join(` ${m.search_and()} `)
                    });
                }
            } catch (err) {
                if (err.name !== 'AbortError') {
                    error = m.search_load_error();
                }
            } finally {
                if (!controller.signal.aborted) {
                    loading = false;
                }
            }
        }

        loadResults();

        return () => controller.abort();
    });
</script>

<svelte:head>
    <title>{m.search_title()} | NextJob</title>
    <meta
        name="description"
        content={m.search_meta_description()}
    />
</svelte:head>

<div class="search-page">
    <div class="page-container">

        <header class="page-header">
            <span class="eyebrow">NEXTJOB / {m.search_discover_label()}</span>

            <h1>
                {m.search_heading_first()}
                <span>{m.search_heading_second()}</span>
            </h1>

            <p>
                {m.search_intro()}
            </p>
        </header>

        <form class="main-search" onsubmit={submitSearch}>
            <Search size={22} strokeWidth={1.7} />

            <input
                type="search"
                bind:value={searchInput}
                placeholder={m.search_placeholder()}
                aria-label={m.search_term_label()}
            />

            <button type="submit">
                {m.search_button()}
                <ArrowUpRight size={19} />
            </button>
        </form>

        <div class="filter-row">
            <div class="filter-buttons">
                <button
                    type="button"
                    class:active={selectedCategory === 'all'}
                    onclick={() => changeCategory('all')}
                >
                    {m.search_all()}
                </button>

                <button
                    type="button"
                    class:active={selectedCategory === 'jobs'}
                    onclick={() => changeCategory('jobs')}
                >
                    <BriefcaseBusiness size={17} />
                    {m.search_jobs()}
                </button>

                <button
                    type="button"
                    class:active={selectedCategory === 'users'}
                    onclick={() => changeCategory('users')}
                >
                    <UserRound size={17} />
                    {m.search_workers()}
                </button>
            </div>

            {#if !loading}
                <span class="result-count">
                    {totalResults}
                    {totalResults === 1
                        ? m.search_result_singular()
                        : m.search_result_plural()}
                </span>
            {/if}
        </div>

        {#if loading}
            <div class="state-message">
                <LoaderCircle size={30} class="loading-icon" />
                <p>{m.search_loading()}</p>
            </div>
        {:else}
            {#if error}
                <div class="error-message" role="alert">
                    <AlertCircle size={19} />
                    <span>{error}</span>
                </div>
            {/if}

            {#if totalResults === 0}
                <div class="empty-state">
                    <Search size={35} strokeWidth={1.4} />

                    <h2>{m.search_empty_title()}</h2>

                    <p>
                        {m.search_empty_description()}
                    </p>
                </div>
            {:else}
                {#if visibleProblems.length > 0}
                    <section class="results-section">
                        <div class="section-heading">
                            <div>
                                <span class="section-label">{m.search_orders_label()}</span>
                                <h2>{m.search_discover_jobs()}</h2>
                            </div>

                            <span class="section-count">
                                {visibleProblems.length}
                            </span>
                        </div>

                        <div class="results-grid">
                            {#each visibleProblems as job, index (job.problem_id ?? `job-${index}`)}
                                <article class="result-card">
                                    <div class="card-top">
                                        <span class="card-type">
                                            <BriefcaseBusiness size={15} />
                                            {m.search_job_singular()}
                                        </span>

                                        {#if job.status === 'open'}
                                            <span class="status">
                                                {m.search_open()}
                                            </span>
                                        {/if}
                                    </div>

                                    <h3>{(job.title_localized ?? job.title)}</h3>

                                    <p class="card-description">
                                        {(job.category_localized ?? job.category) || m.search_service()}
                                    </p>

                                    <div class="card-footer">
                                        <span class="location">
                                            <MapPin size={16} />
                                            {job.neighborhood || 'Shkodër'}
                                        </span>

                                        {#if job.budget !== null && job.budget !== undefined}
                                            <span class="price">
                                                {Number(job.budget).toLocaleString('de-DE')}
                                                ALL
                                            </span>
                                        {/if}
                                    </div>
                                </article>
                            {/each}
                        </div>
                    </section>
                {/if}

                {#if visibleWorkers.length > 0}
                    <section class="results-section">
                        <div class="section-heading">
                            <div>
                                <span class="section-label">{m.search_workers_label()}</span>
                                <h2>{m.search_experienced_people()}</h2>
                            </div>

                            <span class="section-count">
                                {visibleWorkers.length}
                            </span>
                        </div>

                        <div class="results-grid">
                            {#each visibleWorkers as worker, index (worker.worker_id ?? `worker-${index}`)}
                                <article class="result-card worker-card">
                                    <div class="worker-heading">
                                        <div class="worker-avatar">
                                            {(worker.full_name || '?')
                                                .charAt(0)
                                                .toUpperCase()}
                                        </div>

                                        <div>
                                            <span class="card-type">
                                                <UserRound size={14} />
                                                {m.search_worker_singular()}
                                            </span>

                                            <h3>
                                                {worker.full_name || m.search_worker_singular()}
                                            </h3>
                                        </div>
                                    </div>

                                    <p class="card-description">
                                        {(worker.headline_localized ?? worker.headline) || m.search_local_worker()}
                                    </p>

                                    <div class="card-footer">
                                        <span class="location">
                                            <MapPin size={16} />
                                            {worker.neighborhood || 'Shkodër'}
                                        </span>

                                        {#if Number(worker.avg_rating) > 0}
                                            <span class="rating">
                                                ★ {Number(worker.avg_rating).toFixed(1)}
                                            </span>
                                        {/if}
                                    </div>

                                    {#if worker.worker_id != null}
                                        <a
                                            href={resolve(`/chat/${worker.worker_id}`)}
                                            class="chat-worker-button"
                                            aria-label={`${m.chat_send()} – ${worker.full_name || m.search_worker_singular()}`}
                                        >
                                            <MessageCircle size={18} />
                                            {m.chat_send()}
                                        </a>
                                    {/if}
                                </article>
                            {/each}
                        </div>
                    </section>
                {/if}
            {/if}
        {/if}
    </div>
</div>


   



<style>
 .chat-worker-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 10px;
        width: 100%;
        margin-top: 18px;
        padding: 13px 18px;
        background: var(--color-charcoal);
        color: white;
        font-size: 13px;
        font-weight: 600;
        text-decoration: none;
        transition: background-color 0.2s ease;
    }

    .chat-worker-button:hover,
    .chat-worker-button:focus-visible {
        background: var(--color-fresh);
    }

    .search-page {
        min-height: 100vh;
        background: var(--color-off-white);
        color: var(--color-charcoal);
        font-family: var(--font-body);
    }

    .page-container {
        max-width: 1350px;
        margin: 0 auto;
        padding: 75px clamp(24px, 5vw, 80px) 110px;
    }

    .page-header {
        max-width: 780px;
        margin-bottom: 40px;
    }

    .eyebrow,
    .section-label {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.17em;
        color: var(--color-charcoal);
        opacity: 0.65;
    }

    .page-header h1 {
        margin: 18px 0;
        font-family: var(--font-display);
        font-size: clamp(42px, 5.5vw, 76px);
        font-weight: 700;
        letter-spacing: -0.055em;
        line-height: 1.08;
    }

    .page-header h1 span {
        color: var(--color-fresh);
    }

    .page-header p {
        max-width: 520px;
        font-size: 16px;
        line-height: 1.8;
        opacity: 0.7;
    }

    .main-search {
        display: flex;
        align-items: center;
        gap: 16px;
        max-width: 900px;
        padding: 9px 10px 9px 22px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 18%, transparent);
        background: color-mix(
            in srgb,
            var(--color-sage) 10%,
            var(--color-off-white)
        );
    }

    .main-search input {
        flex: 1;
        min-width: 0;
        padding: 13px 0;
        border: 0;
        outline: 0;
        background: transparent;
        color: var(--color-charcoal);
        font-family: inherit;
        font-size: 15px;
    }

    .main-search input::placeholder {
        color: var(--color-charcoal);
        opacity: 0.5;
    }

    .main-search button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 15px;
        min-height: 47px;
        padding: 12px 21px;
        border: 0;
        background: var(--color-charcoal);
        color: var(--color-off-white);
        font-family: inherit;
        font-size: 13px;
        font-weight: 600;
        cursor: pointer;
    }

    .main-search button:hover {
        background: var(--color-fresh);
        color: var(--color-charcoal);
    }

    .filter-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 15px;
        flex-wrap: wrap;
        margin: 28px 0 45px;
    }

    .filter-buttons {
        display: flex;
        gap: 9px;
        flex-wrap: wrap;
    }

    .filter-buttons button {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 11px 17px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 18%, transparent);
        background: transparent;
        color: var(--color-charcoal);
        font-family: inherit;
        font-size: 13px;
        cursor: pointer;
        transition: background 0.2s;
    }

    .filter-buttons button:hover {
        background: var(--color-sage);
    }

    .filter-buttons button.active {
        background: var(--color-charcoal);
        color: var(--color-off-white);
        border-color: var(--color-charcoal);
    }

    .result-count {
        font-size: 13px;
        opacity: 0.6;
    }

    .results-section {
        margin-bottom: 65px;
    }

    .section-heading {
        display: flex;
        align-items: end;
        justify-content: space-between;
        gap: 20px;
        margin-bottom: 25px;
        padding-bottom: 18px;
        border-bottom: 1px solid
            color-mix(in srgb, var(--color-charcoal) 16%, transparent);
    }

    .section-heading h2 {
        margin: 9px 0 0;
        font-family: var(--font-display);
        font-size: clamp(26px, 3vw, 37px);
        letter-spacing: -0.04em;
    }

    .section-count {
        font-size: 15px;
        font-weight: 600;
        opacity: 0.6;
    }

    .results-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 20px;
    }

    .result-card {
        display: flex;
        flex-direction: column;
        min-height: 220px;
        padding: 26px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 13%, transparent);
        background: color-mix(
            in srgb,
            var(--color-sage) 7%,
            var(--color-off-white)
        );
        transition: border-color 0.2s, transform 0.2s;
    }

    .result-card:hover {
        border-color: var(--color-fresh);
        transform: translateY(-3px);
    }

    .card-top {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
        margin-bottom: 25px;
    }

    .card-type {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-size: 11px;
        font-weight: 600;
        opacity: 0.65;
    }

    .status {
        padding: 6px 10px;
        background: var(--color-sage);
        font-size: 11px;
        font-weight: 600;
    }

    .result-card h3 {
        margin: 0 0 12px;
        font-family: var(--font-display);
        font-size: 21px;
        font-weight: 600;
        line-height: 1.3;
        letter-spacing: -0.025em;
        overflow-wrap: anywhere;
    }

    .card-description {
        margin: 0 0 25px;
        font-size: 13px;
        line-height: 1.7;
        opacity: 0.65;
    }

    .card-footer {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: auto;
        padding-top: 17px;
        border-top: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    }

    .location {
        display: inline-flex;
        align-items: center;
        gap: 7px;
        font-size: 12px;
        opacity: 0.7;
    }

    .price,
    .rating {
        font-size: 13px;
        font-weight: 700;
    }

    .worker-heading {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 22px;
    }

    .worker-heading h3 {
        margin: 7px 0 0;
    }

    .worker-avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 55px;
        height: 55px;
        flex-shrink: 0;
        background: var(--color-sage);
        font-family: var(--font-display);
        font-size: 23px;
        font-weight: 600;
    }

    .state-message,
    .empty-state {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 16px;
        padding: 85px 25px;
        text-align: center;
    }

    .state-message p,
    .empty-state p {
        max-width: 400px;
        font-size: 14px;
        line-height: 1.7;
        opacity: 0.65;
    }

    .empty-state h2 {
        margin: 10px 0 0;
        font-family: var(--font-display);
        font-size: 28px;
    }

    .error-message {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 25px;
        padding: 16px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 20%, transparent);
        font-size: 13px;
    }

    .loading-icon {
        animation: spin 1s linear infinite;
    }

    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }

    @media (max-width: 1000px) {
        .results-grid {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
    }

    @media (max-width: 650px) {
        .page-container {
            padding-top: 45px;
        }

        .results-grid {
            grid-template-columns: 1fr;
        }

        .main-search {
            gap: 10px;
            padding-left: 14px;
        }

        .main-search button {
            padding-inline: 12px;
            gap: 6px;
        }

        .result-card {
            min-height: 195px;
        }
    }
</style>
