<script>
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

    // Text vereinheitlichen: Kleinbuchstaben, keine Akzente
    function normalizeText(value) {
        return String(value ?? '')
            .toLocaleLowerCase()
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim();
    }

    // Alle Texte eines Auftrags für die Suche zusammenführen
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

    // Wörter aus dem Suchtext bilden
    function getWords(text) {
        return normalizeText(text)
            .split(/[\s,.;:!?/\\()[\]{}_-]+/)
            .filter(Boolean);
    }

    // Editierdistanz mit Unterstützung für vertauschte Nachbarzeichen
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

                // Zwei benachbarte Buchstaben wurden vertauscht
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

    // Prüfen, ob ein Suchbegriff zu einem Wort passt
    function wordMatches(term, word) {
        if (word.includes(term) || term.includes(word)) {
            return true;
        }

        // Tippfehlertoleranz erst bei längeren Wörtern,
        // damit kurze Begriffe nicht zu viele falsche Treffer liefern
        if (term.length < 4 || word.length < 4) {
            return false;
        }

        const maxDistance =
            term.length >= 8 ? 2 : 1;

        // Wörter mit stark unterschiedlicher Länge ausschließen
        if (Math.abs(term.length - word.length) > maxDistance) {
            return false;
        }

        return editDistance(term, word) <= maxDistance;
    }

    // Alle Suchbegriffe müssen irgendwo im Auftrag vorkommen
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

    // Suchergebnisse live berechnen
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

    // Pagination
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
    <title>Jobnehmer | NextJob</title>
    <meta
        name="description"
        content="Entdecke passende Aufträge auf NextJob."
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <!-- HEADER -->
    <header
        class="sticky top-0 z-20 border-b border-[#2A2E38]/10 bg-white/95 backdrop-blur"
    >
    </header>

        <!-- HAUPTBEREICH -->
<main class="mx-auto max-w-7xl px-4 py-6 sm:px-6 sm:py-8">
        <!-- WILLKOMMEN -->
        <section class="mb-8">
            <p
                class="mb-2 text-sm font-semibold uppercase tracking-wider text-[#62AA97]"
            >
                Für dich
            </p>

            <h1 class="text-2xl font-bold tracking-tight sm:text-4xl">
                Willkommen bei NextJob {data.user?.first_name ?? ''} 
            </h1>

            <p
                class="mt-2 max-w-2xl text-sm leading-6 text-[#2A2E38]/60 sm:text-base"
            >
                Entdecke passende Aufträge und finde Jobs, die zu deinen
                Fähigkeiten und deinem Standort passen.
            </p>
        </section>

        <!-- FEHLERMELDUNG -->
        {#if data.error}
            <div
                class="mb-6 rounded-2xl border border-[#8FB0C4]/40 bg-[#8FB0C4]/20 px-5 py-4"
                role="status"
            >
                <p class="font-medium">{data.error}</p>
            </div>
        {/if}

        <!-- VERBESSERTE SUCHE -->
        <section class="mb-8">
            <label
                for="job-search"
                class="mb-2 block text-sm font-semibold"
            >
                Aufträge suchen
            </label>

            <div class="relative">
                <span
                    class="pointer-events-none absolute left-4 top-1/2 -translate-y-1/2 text-[#2A2E38]/40"
                    aria-hidden="true"
                >
                    🔍
                </span>

                <input
                    id="job-search"
                    type="search"
                    value={search}
                    oninput={(event) =>
                        updateSearch(event.currentTarget.value)}
                    placeholder="z. B. painter, Shkodra ..."
                    autocomplete="off"
                    class="w-full rounded-2xl border border-[#2A2E38]/10 bg-white py-4 pl-11 pr-12 outline-none transition focus:border-[#62AA97] focus:ring-2 focus:ring-[#62AA97]/20"
                />

                {#if search}
                    <button
                        type="button"
                        onclick={() => updateSearch('')}
                        aria-label="Suchtext löschen"
                        class="absolute right-3 top-1/2 -translate-y-1/2 rounded-lg px-3 py-2 text-sm text-[#2A2E38]/60 transition hover:bg-[#F5F1EE] hover:text-[#2A2E38]"
                    >
                        ✕
                    </button>
                {/if}
            </div>

            <p class="mt-2 text-xs leading-5 text-[#2A2E38]/50">
                Suche nach Wörtern oder Wortteilen. Leichte Tippfehler
                werden bei längeren Wörtern berücksichtigt.
            </p>
        </section>
        
                <!-- KATEGORIEN -->
        <section class="mb-8">
            <div class="flex gap-2 overflow-x-auto pb-2">
                {#each categories as category}
                    <button
                        type="button"
                        onclick={() => updateCategory(category)}
                        aria-pressed={selectedCategory === category}
                        class={`shrink-0 rounded-full border px-4 py-2 text-sm font-medium transition ${
                            selectedCategory === category
                                ? 'border-[#62AA97] bg-[#62AA97] text-white'
                                : 'border-[#2A2E38]/10 bg-white hover:border-[#62AA97]'
                        }`}
                    >
                        {category}
                    </button>
                {/each}
            </div>
        </section>

               <!-- INHALT UND SIDEBAR -->
        <div class="grid gap-8 lg:grid-cols-[minmax(0,1fr)_300px]">
            <!-- AUFTRÄGE -->
            <section class="min-w-0">
                <div
                    class="mb-5 flex flex-wrap items-end justify-between gap-3"
                >
                    <div>
                        <h2 class="text-2xl font-bold">
                            Passende Aufträge
                        </h2>

                        <p class="mt-1 text-sm text-[#2A2E38]/50">
                            Empfehlungen für dich
                        </p>
                    </div>

                    <span
                        class="rounded-full bg-[#A8B79E]/40 px-3 py-1 text-xs font-semibold"
                    >
                        {filteredJobs.length}
                        {filteredJobs.length === 1 ? 'Job' : 'Jobs'}
                    </span>
                </div>

                {#if paginatedJobs.length > 0}
                    <!-- AUFTRAGSKARTEN -->
                    <div class="grid gap-5 sm:grid-cols-2">
                        {#each paginatedJobs as job, index (`${job.problem_id ?? job.id ?? index}`)}
                            <article
                                class="group flex min-w-0 flex-col overflow-hidden rounded-2xl border border-[#2A2E38]/10 bg-white shadow-sm transition hover:-translate-y-1 hover:shadow-lg"
                            >
                                <div class="flex-1 p-5">
                                    <div
                                        class="mb-4 flex items-start justify-between gap-3"
                                    >
                                        <div
                                            class="flex h-11 w-11 shrink-0 items-center justify-center rounded-xl bg-[#A8B79E]/50"
                                        >
                                            💼
                                        </div>

                                        {#if job.urgency === 'high' || job.urgency === 'emergency'}
                                            <span
                                                class="rounded-full bg-[#62AA97]/15 px-3 py-1 text-xs font-bold text-[#398875]"
                                            >
                                                Dringend
                                            </span>
                                        {:else}
                                            <span
                                                class="rounded-full bg-[#8FB0C4]/20 px-3 py-1 text-xs font-medium"
                                            >
                                                Offen
                                            </span>
                                        {/if}
                                    </div>

                                    <h3
                                        class="break-words text-lg font-bold"
                                    >
                                        {job.title ?? 'Ohne Titel'}
                                    </h3>

                                    <p
                                        class="mt-2 break-words text-sm leading-6 text-[#2A2E38]/60"
                                    >
                                        {job.description ??
                                            'Keine Beschreibung vorhanden.'}
                                    </p>

                                    <div class="mt-5 space-y-2">
                                        {#if job.location}
                                            <div
                                                class="flex items-start gap-2 text-sm"
                                            >
                                                <span>📍</span>
                                                <span
                                                    class="break-words text-[#2A2E38]/70"
                                                >
                                                    {job.location}
                                                </span>
                                            </div>
                                        {/if}

                                        {#if job.budget != null && job.budget !== ''}
                                            <div
                                                class="flex items-start gap-2 text-sm"
                                            >
                                                <span>💰</span>
                                                <span class="font-semibold">
                                                    {job.budget}
                                                </span>
                                            </div>
                                        {/if}

                                        {#if getCategory(job)}
                                            <div
                                                class="flex items-start gap-2 text-sm"
                                            >
                                                <span>🏷️</span>
                                                <span
                                                    class="break-words text-[#2A2E38]/70"
                                                >
                                                    {getCategory(job)}
                                                </span>
                                            </div>
                                        {/if}
                                    </div>
                                </div>

                                <div class="p-5 pt-0">
                                    <a
                                        href={`/jobs/${job.problem_id ?? job.id}`}
                                        class="flex w-full items-center justify-center rounded-xl bg-[#62AA97] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                                    >
                                        Auftrag ansehen
                                    </a>
                                </div>
                            </article>
                        {/each}
                    </div>
                <!-- PAGINATION -->
                    {#if totalPages > 1}
                        <nav
                            class="mt-8 flex flex-wrap items-center justify-center gap-2"
                            aria-label="Seitennavigation für Aufträge"
                        >
                            <button
                                type="button"
                                onclick={() => goToPage(currentPage - 1)}
                                disabled={currentPage === 1}
                                class="rounded-xl border border-[#2A2E38]/10 bg-white px-3 py-2 text-sm font-semibold transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                            >
                                ← Zurück
                            </button>

                            {#each pageNumbers as page}
                                <button
                                    type="button"
                                    onclick={() => goToPage(page)}
                                    aria-label={`Seite ${page}`}
                                    aria-current={currentPage === page
                                        ? 'page'
                                        : undefined}
                                    class={`h-10 min-w-10 rounded-xl border px-3 text-sm font-semibold transition ${
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
                                class="rounded-xl border border-[#2A2E38]/10 bg-white px-3 py-2 text-sm font-semibold transition hover:border-[#62AA97] disabled:cursor-not-allowed disabled:opacity-40"
                            >
                                Weiter →
                            </button>
                        </nav>

                        <p
                            class="mt-3 text-center text-xs text-[#2A2E38]/50"
                        >
                            Seite {currentPage} von {totalPages}
                        </p>
                    {/if} 
                {:else}  
                    <!-- LEERE SUCHERGEBNISSE -->
                    <div
                        class="rounded-2xl border border-dashed border-[#2A2E38]/15 bg-white px-5 py-12 text-center sm:px-6 sm:py-16"
                    >
                        <div class="mx-auto mb-4 text-5xl">
                            🔎
                        </div>

                        <h3 class="text-lg font-bold">
                            {search.trim() || selectedCategory !== 'Alle'
                                ? 'Keine passenden Aufträge gefunden'
                                : 'Aktuell keine Aufträge verfügbar'}
                        </h3>

                        <p
                            class="mx-auto mt-2 max-w-md text-sm leading-6 text-[#2A2E38]/50"
                        >
                            {search.trim() || selectedCategory !== 'Alle'
                                ? 'Versuche einen anderen Suchbegriff oder setze die Suche zurück.'
                                : 'Schau später wieder vorbei. Neue Aufträge können jederzeit hinzukommen.'}
                        </p>

                        {#if search.trim() || selectedCategory !== 'Alle'}
                            <button
                                type="button"
                                onclick={resetFilters}
                                class="mt-5 rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                            >
                                Suche zurücksetzen
                            </button>
                        {/if}
                    </div>
                {/if}
            </section> 
            
            <!-- SIDEBAR -->
            <aside class="space-y-5">
                <!-- PROFIL -->
                <section
                    class="rounded-2xl bg-[#2A2E38] p-5 text-white sm:p-6"
                >
                    <div class="flex items-center gap-4">
                        <div
                            class="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-[#A8B79E] text-xl font-bold text-[#2A2E38]"
                        >
                            {data.user?.first_name?.charAt(0) ?? 'U'}
                        </div>

                        <div class="min-w-0">
                            <h3 class="break-words font-bold">
                                {data.user?.first_name ?? ''}
                                {data.user?.last_name ?? ''}
                            </h3>

                            <p class="text-sm text-white/60">
                                Jobnehmer
                            </p>
                        </div>
                    </div>

                    <a
                        href="/profile"
                        class="mt-5 block rounded-xl bg-[#A8B79E] px-4 py-3 text-center text-sm font-bold text-[#2A2E38] transition hover:bg-[#8fa18a]"
                    >
                        Profil ansehen
                    </a>
                </section>

                <!-- FOLLOW -->
                <section
                    class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-6"
                >
                    <div class="mb-4 flex items-center gap-3">
                        <div
                            class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#8FB0C4]/30"
                        >
                            ⭐
                        </div>

                        <div>
                            <h3 class="font-bold">Meine Folgen</h3>

                            <p class="text-xs text-[#2A2E38]/50">
                                Gefolgte Nutzer
                            </p>
                        </div>
                    </div>

                    <p class="text-sm leading-6 text-[#2A2E38]/60">
                        Folge interessanten Jobnehmern oder Jobgebern
                        und behalte ihre Aktivitäten im Blick.
                    </p>

                    <a
                        href="/profile"
                        class="mt-4 block w-full rounded-xl border border-[#62AA97] px-4 py-3 text-center text-sm font-semibold text-[#398875] transition hover:bg-[#62AA97] hover:text-white"
                    >
                        Folgen verwalten
                    </a>
                </section>

                <!-- GESPEICHERTE JOBS -->
                <section
                    class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-6"
                >
                    <div
                        class="mb-3 flex items-center justify-between gap-3"
                    >
                        <h3 class="font-bold">
                            Gespeicherte Jobs
                        </h3>

                        <span
                            class="flex h-7 min-w-7 items-center justify-center rounded-full bg-[#A8B79E]/40 px-2 text-xs font-bold"
                        >
                            {data.savedJobs?.length ?? 0}
                        </span>
                    </div>

                    <p class="text-sm leading-6 text-[#2A2E38]/50">
                        Speichere interessante Aufträge, um sie später
                        schnell wiederzufinden.
                    </p>

                    <a
                        href="/saved"
                        class="mt-4 block text-sm font-bold text-[#398875] hover:underline"
                    >
                        Gespeicherte Jobs →
                    </a>
                </section>

                <!-- BEITRAG -->
                <section
                    class="rounded-2xl bg-[#A8B79E]/35 p-5 sm:p-6"
                >

                    <h3 class="font-bold">Dein Beitrag</h3>

                    <p class="mt-2 text-sm leading-6 text-[#2A2E38]/60">
                        Teile deine Erfahrungen und Aktivitäten auf
                        NextJob.
                    </p>

                    <a
                        href="/jobnehmerProfile"
                        class="mt-4 inline-block rounded-xl bg-[#2A2E38] px-4 py-3 text-sm font-bold text-white transition hover:bg-[#1e222b]"
                    >
                        Profil öffnen
                    </a>
                </section>
            </aside>
        </div>
    </main>
</div>