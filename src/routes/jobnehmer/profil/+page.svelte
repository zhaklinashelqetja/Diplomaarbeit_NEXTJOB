<script>
    let { data } = $props();

    let user = $derived(data.user);

    let firstName = $derived(user?.first_name ?? '');
    let lastName = $derived(user?.last_name ?? '');
    let fullName = $derived(
        `${firstName} ${lastName}`.trim() || 'Jobnehmer'
    );

    let initials = $derived(
        `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase() ||
            'U'
    );

    let bio = $derived(
        user?.bio ?? user?.about ?? user?.description ?? ''
    );

    let location = $derived(
        user?.location ?? user?.city ?? ''
    );

    let skills = $derived.by(() => {
        const value = user?.skills;

        if (Array.isArray(value)) {
            return value
                .map((skill) =>
                    typeof skill === 'string' ? skill : skill?.name
                )
                .filter(Boolean);
        }

        if (typeof value === 'string' && value.trim()) {
            return value
                .split(',')
                .map((skill) => skill.trim())
                .filter(Boolean);
        }

        return [];
    });

    let profileFields = $derived([
        firstName,
        lastName,
        user?.email,
        location,
        bio,
        skills.length > 0
    ]);

    let completedFields = $derived(
        profileFields.filter(Boolean).length
    );

    let profileProgress = $derived(
        Math.round((completedFields / profileFields.length) * 100)
    );
</script>

<svelte:head>
    <title>Mein Profil | NextJob</title>
    <meta
        name="description"
        content="Dein persönliches Jobnehmer-Profil auf NextJob."
    />
</svelte:head>

    <main class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-10">
        {#if data.error}
            <section
                class="rounded-2xl border border-[#8FB0C4]/40 bg-white p-6 sm:p-8"
                role="alert"
            >
                <h1 class="text-xl font-bold">Profil nicht verfügbar</h1>

                <p class="mt-2 text-sm leading-6 text-[#2A2E38]/65">
                    {data.error}
                </p>

                <a
                    href="/jobnehmer"
                    class="mt-5 inline-flex rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                >
                    Zur Jobnehmer-Hauptseite
                </a>
            </section>
        {:else if user}
            <!-- SEITENÜBERSCHRIFT -->
            <section class="mb-7">
                <p
                    class="text-sm font-semibold uppercase tracking-wider text-[#398875]"
                >
                    Mein Bereich
                </p>

                <h1 class="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
                    Mein Profil
                </h1>

                <p class="mt-2 text-sm leading-6 text-[#2A2E38]/60 sm:text-base">
                    Präsentiere deine Fähigkeiten und zeige anderen,
                    welche Dienstleistungen du anbietest.
                </p>
            </section>

            <!-- PROFILKOPF -->
            <section
                class="overflow-hidden rounded-2xl border border-[#2A2E38]/10 bg-white shadow-sm"
            >
                <div class="h-28 bg-[#A8B79E] sm:h-36"></div>

                <div class="px-5 pb-6 sm:px-8 sm:pb-8">
                    <div
                        class="-mt-12 flex flex-col gap-5 sm:-mt-14 sm:flex-row sm:items-end sm:justify-between"
                    >
                        <div class="flex min-w-0 items-end gap-4">
                            <div
                                class="flex h-24 w-24 shrink-0 items-center justify-center rounded-2xl border-4 border-white bg-[#8FB0C4] text-3xl font-bold text-[#2A2E38] sm:h-28 sm:w-28 sm:text-4xl"
                                aria-label={`Initialen von ${fullName}`}
                            >
                                {initials}
                            </div>

                            <div class="min-w-0 pb-1">
                                <h2 class="break-words text-xl font-bold sm:text-2xl">
                                    {fullName}
                                </h2>

                                <p class="mt-1 text-sm text-[#2A2E38]/60">
                                    Jobnehmer
                                </p>

                                {#if location}
                                    <p class="mt-2 flex items-center gap-2 text-sm text-[#2A2E38]/70">
                                        <span aria-hidden="true">📍</span>
                                        <span>{location}</span>
                                    </p>
                                {/if}
                            </div>
                        </div>

                        <a
                            href="/jobnehmer"
                            class="inline-flex items-center justify-center rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                        >
                            Aufträge entdecken
                        </a>
                    </div>
                </div>
            </section>