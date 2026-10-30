<script>
    import { t } from '$lib/i18n.js';

    let { data } = $props();

    let user = $derived(data.user);

    let firstName = $derived(user?.first_name ?? '');
    let lastName = $derived(user?.last_name ?? '');
    let fullName = $derived(
        `${firstName} ${lastName}`.trim() || $t('worker_role')
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
    <title>{$t('profile_title')} | NextJob</title>
    <meta
        name="description"
        content={$t('profile_meta_description')}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-6xl px-4 py-6 sm:px-6 sm:py-10">
        {#if data.error}
            <section
                class="rounded-2xl border border-[#8FB0C4]/40 bg-white p-6 sm:p-8"
                role="alert"
            >
                <h1 class="text-xl font-bold">
                    {$t('profile_unavailable')}
                </h1>

                <p class="mt-2 text-sm leading-6 text-[#2A2E38]/65">
                    {data.error}
                </p>

                <a
                    href="/jobnehmer"
                    class="mt-5 inline-flex rounded-xl bg-[#62AA97] px-5 py-3 text-sm font-bold text-white transition hover:bg-[#529b88]"
                >
                    {$t('profile_back_to_jobs')}
                </a>
            </section>
        {:else if user}
            <!-- SEITENÜBERSCHRIFT -->
            <section class="mb-7">
                <p
                    class="text-sm font-semibold uppercase tracking-wider text-[#398875]"
                >
                    {$t('profile_my_area')}
                </p>

                <h1 class="mt-2 text-3xl font-bold tracking-tight sm:text-4xl">
                    {$t('profile_title')}
                </h1>

                <p class="mt-2 text-sm leading-6 text-[#2A2E38]/60 sm:text-base">
                    {$t('profile_intro')}
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
                                aria-label={`${$t('profile_initials_of')} ${fullName}`}
                            >
                                {initials}
                            </div>

                            <div class="min-w-0 pb-1">
                                <h2 class="break-words text-xl font-bold sm:text-2xl">
                                    {fullName}
                                </h2>

                                <p class="mt-1 text-sm text-[#2A2E38]/60">
                                    {$t('worker_role')}
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
                            {$t('profile_discover_jobs')}
                        </a>
                    </div>
                </div>
            </section>

            <!-- PROFILINHALT -->
            <div class="mt-6 grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
                <div class="min-w-0 space-y-6">
                    <!-- ÜBER MICH -->
                    <section
                        class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-7"
                    >
                        <h2 class="text-lg font-bold">
                            {$t('profile_about_me')}
                        </h2>

                        {#if bio}
                            <p class="mt-4 whitespace-pre-line break-words text-sm leading-7 text-[#2A2E38]/70">
                                {bio}
                            </p>
                        {:else}
                            <p class="mt-3 text-sm leading-6 text-[#2A2E38]/55">
                                {$t('profile_no_bio')}
                            </p>
                        {/if}
                    </section>

                    <!-- FÄHIGKEITEN -->
                    <section
                        class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-7"
                    >
                        <h2 class="text-lg font-bold">
                            {$t('profile_my_skills')}
                        </h2>

                        {#if skills.length > 0}
                            <div class="mt-4 flex flex-wrap gap-2">
                                {#each skills as skill, index (`${skill}-${index}`)}
                                    <span
                                        class="rounded-full bg-[#A8B79E]/35 px-4 py-2 text-sm font-medium"
                                    >
                                        {skill}
                                    </span>
                                {/each}
                            </div>
                        {:else}
                            <p class="mt-3 text-sm leading-6 text-[#2A2E38]/55">
                                {$t('profile_no_skills')}
                            </p>
                        {/if}
                    </section>

                    <!-- KONTAKT -->
                    <section
                        class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-7"
                    >
                        <h2 class="text-lg font-bold">
                            {$t('profile_contact_info')}
                        </h2>

                        <div class="mt-5 space-y-4">
                            {#if user.email}
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#8FB0C4]/25"
                                    >
                                        <span aria-hidden="true">✉️</span>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-xs font-medium text-[#2A2E38]/50">
                                            {$t('profile_email')}
                                        </p>

                                        <p class="mt-1 break-all text-sm font-medium">
                                            {user.email}
                                        </p>
                                    </div>
                                </div>
                            {/if}

                            {#if user.phone}
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#8FB0C4]/25"
                                    >
                                        <span aria-hidden="true">📞</span>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-xs font-medium text-[#2A2E38]/50">
                                            {$t('profile_phone')}
                                        </p>

                                        <p class="mt-1 break-words text-sm font-medium">
                                            {user.phone}
                                        </p>
                                    </div>
                                </div>
                            {/if}

                            {#if location}
                                <div class="flex items-start gap-3">
                                    <div
                                        class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-[#8FB0C4]/25"
                                    >
                                        <span aria-hidden="true">📍</span>
                                    </div>

                                    <div class="min-w-0">
                                        <p class="text-xs font-medium text-[#2A2E38]/50">
                                            {$t('profile_location')}
                                        </p>

                                        <p class="mt-1 break-words text-sm font-medium">
                                            {location}
                                        </p>
                                    </div>
                                </div>
                            {/if}

                            {#if !user.email && !user.phone && !location}
                                <p class="text-sm leading-6 text-[#2A2E38]/55">
                                    {$t('profile_no_contact')}
                                </p>
                            {/if}
                        </div>
                    </section>
                </div>

                <!-- SIDEBAR -->
                <aside class="space-y-6">
                    <!-- PROFILFORTSCHRITT -->
                    <section
                        class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 sm:p-6"
                    >
                        <h2 class="font-bold">
                            {$t('profile_overview')}
                        </h2>

                        <div class="mt-5 flex items-center justify-between gap-3">
                            <span class="text-sm text-[#2A2E38]/60">
                                {$t('profile_data')}
                            </span>

                            <span class="text-lg font-bold text-[#398875]">
                                {profileProgress} %
                            </span>
                        </div>

                        <div
                            class="mt-3 h-2 overflow-hidden rounded-full bg-[#F5F1EE]"
                            role="progressbar"
                            aria-label={$t('profile_completeness')}
                            aria-valuemin="0"
                            aria-valuemax="100"
                            aria-valuenow={profileProgress}
                        >
                            <div
                                class="h-full rounded-full bg-[#62AA97] transition-all"
                                style={`width: ${profileProgress}%`}
                            ></div>
                        </div>

                        <p class="mt-4 text-sm leading-6 text-[#2A2E38]/60">
                            {$t('profile_progress_description')}
                        </p>
                    </section>

                    <!-- MEIN BEREICH -->
                    <section
                        class="rounded-2xl bg-[#2A2E38] p-5 text-white sm:p-6"
                    >
                        <h2 class="font-bold">
                            {$t('profile_my_area')}
                        </h2>

                        <nav class="mt-4 space-y-1">
                            <a
                                href="/jobnehmer"
                                class="flex items-center justify-between rounded-xl px-3 py-3 text-sm transition hover:bg-white/10"
                            >
                                <span>{$t('profile_discover_jobs')}</span>
                                <span aria-hidden="true">→</span>
                            </a>

                            <a
                                href="/saved"
                                class="flex items-center justify-between rounded-xl px-3 py-3 text-sm transition hover:bg-white/10"
                            >
                                <span>{$t('worker_saved_jobs')}</span>
                                <span aria-hidden="true">→</span>
                            </a>
                        </nav>
                    </section>
                </aside>
            </div>
        {:else}
            <section class="rounded-2xl bg-white p-6">
                <h1 class="text-xl font-bold">
                    {$t('profile_unavailable')}
                </h1>

                <p class="mt-2 text-sm text-[#2A2E38]/60">
                    {$t('profile_load_failed')}
                </p>
            </section>
        {/if}
    </main>
</div>