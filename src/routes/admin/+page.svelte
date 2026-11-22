
<script>
    import RegistrationGrowthChart from '$lib/components/RegistrationGrowthChart.svelte';
    import { goto } from '$app/navigation';

    let { data } = $props();

    const stats = [
        {
            title: 'Nutzer',
            value: data.stats.totalUsers,
            description: 'Registrierte Nutzer',
            color: '#A8B79E',
            icon: '👥'
        },
        {
            title: 'Aktive Jobs',
            value: data.stats.activeJobs,
            description: 'Aktuell laufende Jobs',
            color: '#8FB0C4',
            icon: '💼'
        },
        {
            title: 'Angebote',
            value: data.stats.totalOffers,
            description: 'Eingereichte Angebote',
            color: '#62AA97',
            icon: '📋'
        },
        {
            title: 'Gemeldete Inhalte',
            value: data.stats.reportedContent,
            description: 'Markierte Bewertungen',
            color: '#D6B59C',
            icon: '⚠️'
        }
    ];
</script>

<svelte:head>
    <title>Admin-Dashboard | NextJob</title>
    <meta
        name="description"
        content="Administratives Dashboard der NextJob Plattform"
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
                            NextJob / Administration
                        </p>
                    </div>

                    <h1 class="text-4xl font-semibold leading-tight tracking-tight sm:text-5xl">
                        Plattformübersicht<span class="text-[#62AA97]">.</span>
                    </h1>

                    <p class="mt-4 max-w-xl text-sm leading-7 text-[#2A2E38]/65 sm:text-base">
                        Ein zentraler Überblick über Nutzer, Aufträge und
                        Aktivitäten auf der NextJob Plattform.
                    </p>
                </div>

                <div class="border-l-2 border-[#A8B79E] pl-4">
                    <p class="text-xs uppercase tracking-[0.15em] text-[#2A2E38]/45">
                        Dashboard
                    </p>
                    <p class="mt-1 text-sm font-semibold">
                        Verwaltungsbereich
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
                        01 / Kennzahlen
                    </p>

                    <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                        Plattform in Zahlen
                    </h2>
                </div>

                <p class="text-xs text-[#2A2E38]/45">
                    Aktueller Überblick
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
                    02 / Verwaltung
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    Plattform kontrollieren
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
                                    Verwaltung
                                </p>

                                <h3 class="mt-1 text-xl font-semibold">
                                    Benutzer & Aufträge
                                </h3>
                            </div>
                        </div>

                        <p class="mt-4 text-sm leading-6 text-[#2A2E38]/65">
                            Nutzerkonten verwalten, veröffentlichte Aufträge
                            kontrollieren und Inhalte überprüfen.
                        </p>
                    </div>

                    <button
                        type="button"
                        onclick={() => goto('/admin/verwaltung')}
                        class="flex w-full items-center justify-between gap-5 bg-[#2A2E38] px-6 py-4 text-sm font-semibold text-white transition duration-200 hover:bg-[#62AA97] md:w-auto"
                    >
                        Verwaltung öffnen
                        <span class="text-lg">↗</span>
                    </button>

                </div>
            </div>
        </section>

        <!-- Platform activity -->
        <section class="mt-14">

            <div class="mb-8">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                    03 / Plattformaktivität
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    Einblicke in die Nutzung
                </h2>

                <p class="mt-3 max-w-xl text-sm leading-6 text-[#2A2E38]/60">
                    Welche Dienstleistungen gesucht werden und welche
                    Suchbegriffe die Nutzer auf der Plattform verwenden.
                </p>
            </div>

            <div class="grid gap-10 lg:grid-cols-2">

                <!-- Category demand -->
                <div class="border-t border-[#2A2E38]/15 pt-6">

                    <div class="mb-7 flex items-start justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-semibold">
                                Nachfrage nach Kategorien
                            </h3>

                            <p class="mt-2 text-sm text-[#2A2E38]/55">
                                Offene Jobs nach Dienstleistungsbereich
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
                                            {category.open_problems} Jobs
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
                            Noch keine Kategoriedaten vorhanden.
                        </div>

                    {/if}

                </div>

                <!-- Top searches -->
                <div class="border-t border-[#2A2E38]/15 pt-6">

                    <div class="mb-7 flex items-start justify-between gap-4">
                        <div>
                            <h3 class="text-lg font-semibold">
                                Häufigste Suchbegriffe
                            </h3>

                            <p class="mt-2 text-sm text-[#2A2E38]/55">
                                Suchaktivitäten auf der Plattform
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
                                            Anfragen
                                        </span>
                                    </span>

                                </div>
                            {/each}

                        </div>

                    {:else}

                        <div class="border-b border-[#2A2E38]/10 py-8 text-sm text-[#2A2E38]/50">
                            Noch keine Suchdaten vorhanden.
                        </div>

                    {/if}

                </div>

            </div>
        </section>

        <!-- Growth -->
        <section class="mt-14">

            <div class="mb-8">
                <p class="text-xs font-semibold uppercase tracking-[0.16em] text-[#2A2E38]/45">
                    04 / Entwicklung
                </p>

                <h2 class="mt-2 text-2xl font-semibold tracking-tight">
                    Nutzerwachstum
                </h2>

                <p class="mt-3 max-w-xl text-sm leading-6 text-[#2A2E38]/60">
                    Die Entwicklung der Nutzerregistrierungen im zeitlichen Verlauf.
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
                        Admin-Bereich
                    </span>
                </div>

                <p class="text-xs text-[#2A2E38]/45">
                    Plattformverwaltung · Shkodër
                </p>

            </div>

        </footer>

    </main>
</div>
