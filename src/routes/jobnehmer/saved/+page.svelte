<script>
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
    <title>Gespeicherte Jobs | NextJob</title>
    <meta
        name="description"
        content="Finde deine gespeicherten Aufträge auf NextJob wieder."
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <!-- HEADER -->
    <header class="border-b border-[#2A2E38]/10 bg-white">
        <div
            class="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-4 sm:px-6"
        >
            <a
                href="/"
                class="shrink-0 text-2xl font-extrabold tracking-tight"
            >
                NEXT<span class="text-[#62AA97]">J</span>OB
            </a>

            <nav class="flex items-center gap-4 text-sm sm:gap-6">
                <a
                    href="/jobnehmerHauptseite"
                    class="font-medium text-[#2A2E38]/65 transition hover:text-[#62AA97]"
                >
                    Jobs
                </a>

                <a
                    href="/profile"
                    class="hidden font-medium text-[#2A2E38]/65 transition hover:text-[#62AA97] sm:inline"
                >
                    Profil
                </a>

                <a
                    href="/gespeicherteJobs"
                    aria-current="page"
                    class="font-semibold text-[#398875]"
                >
                    Gespeichert
                </a>
            </nav>

            <div
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#A8B79E] font-bold"
                title={data.user?.first_name ?? 'Benutzer'}
            >
                {data.user?.first_name?.charAt(0) ?? 'U'}
            </div>
        </div>
    </header>
