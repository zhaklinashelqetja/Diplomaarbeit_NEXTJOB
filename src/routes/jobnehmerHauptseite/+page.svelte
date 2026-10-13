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
        <div
            class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6"
        >
            <a
                href="/"
                class="shrink-0 text-2xl font-extrabold tracking-tight text-[#2A2E38]"
            >
                NEXT<span class="text-[#62AA97]">J</span>OB
            </a>

            <!-- Desktop Navigation -->
            <nav class="hidden items-center gap-6 md:flex">
                <a
                    href="/jobnehmer"
                    class="font-semibold text-[#62AA97]"
                >
                    Jobs
                </a>

                <a
                    href="/profile"
                    class="text-[#2A2E38]/60 transition hover:text-[#62AA97]"
                >
                    Profil
                </a>

                <a
                    href="/saved"
                    class="text-[#2A2E38]/60 transition hover:text-[#62AA97]"
                >
                    Gespeichert
                </a>
            </nav>

            <!-- Benutzer -->
            <div class="flex items-center gap-3">
                <div
                    class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#A8B79E] font-bold text-[#2A2E38]"
                >
                    {data.user?.first_name?.charAt(0) ?? 'U'}
                </div>

                <div class="hidden sm:block">
                    <p class="text-sm font-semibold">
                        {data.user?.first_name ?? 'User'}
                    </p>

                    <p class="text-xs text-[#2A2E38]/50">
                        Jobnehmer
                    </p>
                </div>
            </div>
        </div>

        <!-- Mobile Navigation -->
        <nav
            class="flex gap-5 overflow-x-auto border-t border-[#2A2E38]/10 px-4 py-3 text-sm md:hidden"
            aria-label="Mobile Navigation"
        >
            <a
                href="/jobnehmer"
                class="shrink-0 font-semibold text-[#62AA97]"
            >
                Jobs
            </a>

            <a href="/profile" class="shrink-0">
                Profil
            </a>

            <a href="/saved" class="shrink-0">
                Gespeichert
            </a>
        </nav>
    </header>