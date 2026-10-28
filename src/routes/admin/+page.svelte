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

