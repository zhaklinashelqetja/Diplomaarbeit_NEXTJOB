<script>
    import registrationGrowthChart from '$lib/components/registrationGrowthChart.svelte';
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
            color: '#A8B79E',
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

    <!-- Main -->
    <main class="mx-auto max-w-7xl px-6 py-8">

        {#if data.error}
            <div
                class="mb-6 rounded-xl border border-red-200 bg-red-50 px-5 py-4 text-sm text-red-700"
            >
                {data.error}
            </div>
        {/if}


        <!-- Statistics -->
        <section>
            <div class="mb-5">
                <h2 class="text-xl font-bold text-[#2A2E38]">
                    Plattformkennzahlen
                </h2>

                <p class="mt-1 text-sm text-[#2A2E38]/60">
                    Aktueller Überblick über NextJob
                </p>
            </div>

            <div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">

                {#each stats as stat}
                    <div
                        class="group rounded-2xl border border-[#2A2E38]/10 bg-white p-6 shadow-sm transition hover:-translate-y-1 hover:shadow-md"
                    >
                        <div class="flex items-start justify-between">

                            <div
                                class="flex h-12 w-12 items-center justify-center rounded-xl text-xl"
                                style={`background-color: ${stat.color}55`}
                            >
                                {stat.icon}
                            </div>

                            <span class="text-xs font-medium uppercase tracking-wide text-[#2A2E38]/40">
                                NextJob
                            </span>

                        </div>

                        <div class="mt-6">
                            <p class="text-sm font-medium text-[#2A2E38]/60">
                                {stat.title}
                            </p>

                            <p class="mt-1 text-4xl font-bold text-[#2A2E38]">
                                {stat.value}
                            </p>

                            <p class="mt-2 text-xs text-[#2A2E38]/50">
                                {stat.description}
                            </p>
                        </div>

                    </div>
                {/each}

            </div>
        </section>


        <!-- Additional statistics -->
        <section class="mt-10 grid gap-6 lg:grid-cols-2">

            <!-- Category demand -->
            <div class="rounded-2xl border border-[#2A2E38]/10 bg-white p-6 shadow-sm">

                <div class="mb-5">
                    <h2 class="text-lg font-bold text-[#2A2E38]">
                        Nachfrage nach Kategorien
                    </h2>

                    <p class="mt-1 text-sm text-[#2A2E38]/60">
                        Offene Jobs und verfügbare Jobnehmer
                    </p>
                </div>

                {#if data.categoryDemand.length > 0}

                    <div class="space-y-4">

                        {#each data.categoryDemand.slice(0, 5) as category}
                            <div>

                                <div class="mb-2 flex items-center justify-between text-sm">
                                    <span class="font-medium">
                                        {category.name}
                                    </span>

                                    <span class="text-[#2A2E38]/50">
                                        {category.open_problems} offene Jobs
                                    </span>
                                </div>

                                <div class="h-2 overflow-hidden rounded-full bg-[#F5F1EE]">

                                    <div
                                        class="h-full rounded-full bg-[#62AA97]"
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

                    <div class="rounded-xl bg-[#F5F1EE] px-4 py-8 text-center">
                        <p class="text-sm text-[#2A2E38]/50">
                            Noch keine Kategoriedaten vorhanden.
                        </p>
                    </div>

                {/if}

            </div>
