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
        `${firstName.charAt(0)}${lastName.charAt(0)}`.toUpperCase() || 'U'
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

    // EDITING STATES
    let editingBio = $state(false);
    let editingSkills = $state(false);
    let editingContact = $state(false);

    let bioDraft = $state('');
    let skillsDraft = $state('');
    let phoneDraft = $state('');
    let locationDraft = $state('');

    let displayedBio = $state('');
    let displayedSkills = $state([]);
    let displayedPhone = $state('');
    let displayedLocation = $state('');

    let profileImage = $state('');
    let imageInput;

    // INITIALIZATION
    let initializedUserKey = $state('');

    $effect(() => {
        if (!user) return;

        const userKey = String(user.id ?? user.email ?? 'default');

        // Initialize only when the user changes
        if (initializedUserKey === userKey) return;

        initializedUserKey = userKey;

        const storageKey = `nextjob_profile_${userKey}`;

        let saved = {};

        try {
            saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
        } catch (error) {
            console.error('Profil konnte nicht geladen werden:', error);
        }

        displayedBio = saved.bio ?? bio;

        displayedSkills = Array.isArray(saved.skills)
            ? saved.skills
            : skills;

        displayedPhone = saved.phone ?? (user.phone ?? '');

        displayedLocation = saved.location ?? location;

        bioDraft = displayedBio;
        skillsDraft = displayedSkills.join(', ');
        phoneDraft = displayedPhone;
        locationDraft = displayedLocation;

        profileImage =
            saved.profileImage ??
            user.profile_image ??
            user.profile_picture ??
            user.avatar ??
            user.image ??
            '';
    });

    // SAVE PROFILE LOCALLY
    function persistProfile() {
        if (!user) return;

        const userKey = String(user.id ?? user.email ?? 'default');
        const storageKey = `nextjob_profile_${userKey}`;

        const profileData = {
            bio: displayedBio,
            skills: displayedSkills,
            phone: displayedPhone,
            location: displayedLocation,
            profileImage
        };

        try {
            localStorage.setItem(storageKey, JSON.stringify(profileData));
        } catch (error) {
            console.error('Profil konnte nicht lokal gespeichert werden:', error);

            alert(
                'Das Profil konnte nicht gespeichert werden. ' +
                'Möglicherweise ist der Speicherplatz zu groß.'
            );
        }
    }

    // BIO
    function startEditingBio() {
        bioDraft = displayedBio;
        editingBio = true;
    }

    function saveBio() {
        displayedBio = bioDraft.trim();
        editingBio = false;
        persistProfile();
    }

    function cancelBio() {
        bioDraft = displayedBio;
        editingBio = false;
    }

    // SKILLS
    function startEditingSkills() {
        skillsDraft = displayedSkills.join(', ');
        editingSkills = true;
    }

    function saveSkills() {
        displayedSkills = skillsDraft
            .split(',')
            .map((skill) => skill.trim())
            .filter(Boolean);

        editingSkills = false;
        persistProfile();
    }

    function cancelSkills() {
        skillsDraft = displayedSkills.join(', ');
        editingSkills = false;
    }

    // CONTACT
    function startEditingContact() {
        phoneDraft = displayedPhone;
        locationDraft = displayedLocation;
        editingContact = true;
    }

    function saveContact() {
        displayedPhone = phoneDraft.trim();
        displayedLocation = locationDraft.trim();

        editingContact = false;
        persistProfile();
    }

    function cancelContact() {
        phoneDraft = displayedPhone;
        locationDraft = displayedLocation;
        editingContact = false;
    }

    // PROFILE IMAGE
    function openImagePicker() {
        imageInput?.click();
    }

    function handleImageChange(event) {
        const file = event.currentTarget.files?.[0];

        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Bitte wähle eine Bilddatei aus.');
            return;
        }

        const reader = new FileReader();

        reader.onload = () => {
            profileImage = reader.result;
            persistProfile();
        };

        reader.onerror = () => {
            alert('Das Bild konnte nicht geladen werden.');
        };

        reader.readAsDataURL(file);
    }
</script>

<svelte:head>
    <title>{$t('profile_title')} | NextJob</title>
    <meta
        name="description"
        content={$t('profile_meta_description')}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">
    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-10">

        {#if data.error}
            <section
                class="border-l-4 border-[#62AA97] bg-white p-6 sm:p-8"
                role="alert"
            >
                <h1 class="text-2xl font-semibold tracking-tight">
                    {$t('profile_unavailable')}
                </h1>

                <p class="mt-3 text-sm leading-7 text-[#2A2E38]/65">
                    {data.error}
                </p>

                <a
                    href="/jobnehmer/hauptseite"
                    class="mt-6 inline-flex items-center gap-2 bg-[#2A2E38] px-5 py-3 text-sm font-medium text-white transition hover:bg-[#398875]"
                >
                    {$t('profile_back_to_jobs')}
                    <span>↗</span>
                </a>
            </section>

        {:else if user}

            <!-- INTRO -->
            <section class="mb-10">
                <div class="flex flex-col justify-between gap-5 sm:flex-row sm:items-end">
                    <div>
                        <p class="text-xs font-semibold uppercase tracking-[0.22em] text-[#398875]">
                            NEXTJOB / {$t('profile_my_area')}
                        </p>

                        <h1 class="mt-3 text-4xl font-semibold tracking-tight sm:text-5xl">
                            {$t('profile_title')}
                        </h1>

                        <p class="mt-4 max-w-xl text-sm leading-7 text-[#2A2E38]/60 sm:text-base">
                            {$t('profile_intro')}
                        </p>
                    </div>
                </div>
            </section>

            <!-- PROFILE HERO -->
            <section class="overflow-hidden bg-[#2A2E38] text-white">

                <div class="grid md:grid-cols-[260px_minmax(0,1fr)]">

                    <!-- PROFILE PHOTO -->
                    <div class="flex flex-col items-center justify-center bg-[#2A2E38] px-6 py-10 md:border-r md:border-white/10">

                        <div class="relative">
                            {#if profileImage}
                                <img
                                    src={profileImage}
                                    alt="Profilbild"
                                    class="h-36 w-36 rounded-full border-4 border-white/10 object-cover sm:h-40 sm:w-40"
                                />
                            {:else}
                                <div class="flex h-36 w-36 items-center justify-center rounded-full border-4 border-white/10 bg-[#A8B79E] text-4xl font-semibold text-[#2A2E38] sm:h-40 sm:w-40">
                                    {initials}
                                </div>
                            {/if}

                            <button
                                type="button"
                                onclick={openImagePicker}
                                aria-label="Profilbild ändern"
                                class="absolute bottom-1 right-1 flex h-11 w-11 items-center justify-center rounded-full border-2 border-[#2A2E38] bg-[#62AA97] text-[#2A2E38] transition hover:bg-[#A8B79E]"
                            >
                                <svg
                                    xmlns="http://www.w3.org/2000/svg"
                                    width="20"
                                    height="20"
                                    viewBox="0 0 24 24"
                                    fill="none"
                                    stroke="currentColor"
                                    stroke-width="2"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                >
                                    <path d="M14.5 4h-5L7 7H4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V9a2 2 0 0 0-2-2h-3l-2.5-3Z"/>
                                    <circle cx="12" cy="13" r="3"/>
                                </svg>
                            </button>
                        </div>

                        <input
                            bind:this={imageInput}
                            type="file"
                            accept="image/*"
                            class="hidden"
                            onchange={handleImageChange}
                        />

                        <button
                            type="button"
                            onclick={openImagePicker}
                            class="mt-5 text-xs font-medium uppercase tracking-[0.15em] text-[#A8B79E] transition hover:text-white"
                        >
                            Foto ändern ↗
                        </button>
                    </div>

                    <!-- NAME AND INFO -->
                    <div class="flex flex-col justify-center bg-[#2A2E38] p-6 sm:p-10 lg:p-12">
                        <p class="text-xs font-medium uppercase tracking-[0.2em] text-[#A8B79E]">
                            {$t('worker_role')}
                        </p>

                        <h2 class="mt-3 break-words text-3xl font-semibold tracking-tight sm:text-4xl lg:text-5xl">
                            {fullName}
                        </h2>

                        {#if displayedLocation}
                            <div class="mt-4 flex items-center gap-2 text-sm text-white/60">
                                <span aria-hidden="true">📍</span>
                                <span>{displayedLocation}</span>
                            </div>
                        {/if}

                        <div class="mt-8">
                            <a
                                href="/jobnehmer/hauptseite"
                                class="inline-flex items-center gap-3 bg-[#62AA97] px-5 py-3 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#A8B79E]"
                            >
                                {$t('profile_discover_jobs')}
                                <span>↗</span>
                            </a>
                        </div>
                    </div>
                </div>

                <!-- FOOTER -->
                <div class="flex items-center justify-between border-t border-white/10 px-5 py-4 sm:px-8">
                    <span class="text-[10px] uppercase tracking-[0.2em] text-white/40">
                        NEXTJOB / PROFILE
                    </span>

                    <span class="text-xs text-white/40">
                        {displayedSkills.length} Skills
                    </span>
                </div>
            </section>

            <!-- MAIN CONTENT -->
            <div class="mt-10 grid gap-10 lg:grid-cols-[minmax(0,1fr)_300px]">

                <!-- LEFT -->
                <div class="min-w-0 space-y-10">

                    <!-- ABOUT -->
                    <section>
                        <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                            <div class="flex items-center gap-4">
                                <span class="text-xs font-semibold text-[#398875]">01</span>

                                <h2 class="text-xl font-semibold tracking-tight sm:text-2xl">
                                    {$t('profile_about_me')}
                                </h2>
                            </div>

                            {#if !editingBio}
                                <button
                                    type="button"
                                    onclick={startEditingBio}
                                    class="inline-flex w-fit items-center gap-2 text-sm font-medium text-[#398875] transition hover:text-[#2A2E38]"
                                >
                                    <span>✎</span>
                                    Bearbeiten
                                </button>
                            {/if}
                        </div>

                        <div class="mt-5 border-t border-[#2A2E38]/15 pt-6">
                            {#if editingBio}
                                <div class="space-y-4">
                                    <textarea
                                        bind:value={bioDraft}
                                        rows="6"
                                        placeholder="Schreibe etwas über dich, deine Erfahrung und deine Arbeit..."
                                        class="w-full resize-y border border-[#2A2E38]/15 bg-white p-4 text-sm leading-7 outline-none transition focus:border-[#62AA97]"
                                    ></textarea>

                                    <div class="flex flex-wrap gap-3">
                                        <button
                                            type="button"
                                            onclick={saveBio}
                                            class="bg-[#62AA97] px-5 py-3 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#A8B79E]"
                                        >
                                            Änderungen übernehmen
                                        </button>

                                        <button
                                            type="button"
                                            onclick={cancelBio}
                                            class="border border-[#2A2E38]/15 px-5 py-3 text-sm font-medium transition hover:bg-white"
                                        >
                                            Abbrechen
                                        </button>
                                    </div>
                                </div>
                            {:else}
                                {#if displayedBio}
                                    <p class="max-w-3xl whitespace-pre-line break-words text-base leading-8 text-[#2A2E38]/75 sm:text-lg">
                                        {displayedBio}
                                    </p>
                                {:else}
                                    <button
                                        type="button"
                                        onclick={startEditingBio}
                                        class="text-sm leading-7 text-[#2A2E38]/50 transition hover:text-[#398875]"
                                    >
                                        {$t('profile_no_bio')} · Hier klicken, um etwas über dich zu schreiben.
                                    </button>
                                {/if}
                            {/if}
                        </div>
                    </section>

                    <!-- SKILLS -->
                    <section>
                        <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                            <div class="flex items-center gap-4">
                                <span class="text-xs font-semibold text-[#398875]">02</span>

                                <h2 class="text-xl font-semibold tracking-tight sm:text-2xl">
                                    {$t('profile_my_skills')}
                                </h2>
                            </div>

                            {#if !editingSkills}
                                <button
                                    type="button"
                                    onclick={startEditingSkills}
                                    class="inline-flex w-fit items-center gap-2 text-sm font-medium text-[#398875] transition hover:text-[#2A2E38]"
                                >
                                    <span>✎</span>
                                    Bearbeiten
                                </button>
                            {/if}
                        </div>

                        <div class="mt-5 border-t border-[#2A2E38]/15 pt-6">
                            {#if editingSkills}
                                <div class="space-y-4">
                                    <textarea
                                        bind:value={skillsDraft}
                                        rows="3"
                                        placeholder="z. B. Maler, Elektriker, Reparaturen, Gartenarbeit..."
                                        class="w-full resize-y border border-[#2A2E38]/15 bg-white p-4 text-sm leading-7 outline-none transition focus:border-[#62AA97]"
                                    ></textarea>

                                    <p class="text-xs leading-5 text-[#2A2E38]/50">
                                        Trenne deine Fähigkeiten mit Kommas.
                                    </p>

                                    <div class="flex flex-wrap gap-3">
                                        <button
                                            type="button"
                                            onclick={saveSkills}
                                            class="bg-[#62AA97] px-5 py-3 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#A8B79E]"
                                        >
                                            Änderungen übernehmen
                                        </button>

                                        <button
                                            type="button"
                                            onclick={cancelSkills}
                                            class="border border-[#2A2E38]/15 px-5 py-3 text-sm font-medium transition hover:bg-white"
                                        >
                                            Abbrechen
                                        </button>
                                    </div>
                                </div>
                            {:else}
                                {#if displayedSkills.length > 0}
                                    <div class="flex flex-wrap gap-3">
                                        {#each displayedSkills as skill, index (`${skill}-${index}`)}
                                            <span
                                                class="border border-[#2A2E38]/10 bg-white px-4 py-3 text-sm font-medium transition hover:border-[#62AA97] hover:bg-[#A8B79E]/20"
                                            >
                                                {skill}
                                            </span>
                                        {/each}
                                    </div>
                                {:else}
                                    <button
                                        type="button"
                                        onclick={startEditingSkills}
                                        class="text-sm leading-7 text-[#2A2E38]/50 transition hover:text-[#398875]"
                                    >
                                        {$t('profile_no_skills')} · Fähigkeiten hinzufügen
                                    </button>
                                {/if}
                            {/if}
                        </div>
                    </section>

                    <!-- CONTACT -->
                    <section>
                        <div class="flex flex-col justify-between gap-4 sm:flex-row sm:items-center">
                            <div class="flex items-center gap-4">
                                <span class="text-xs font-semibold text-[#398875]">03</span>

                                <h2 class="text-xl font-semibold tracking-tight sm:text-2xl">
                                    {$t('profile_contact_info')}
                                </h2>
                            </div>

                            {#if !editingContact}
                                <button
                                    type="button"
                                    onclick={startEditingContact}
                                    class="inline-flex w-fit items-center gap-2 text-sm font-medium text-[#398875] transition hover:text-[#2A2E38]"
                                >
                                    <span>✎</span>
                                    Bearbeiten
                                </button>
                            {/if}
                        </div>

                        <div class="mt-5 border-t border-[#2A2E38]/15 pt-6">

                            {#if editingContact}
                                <div class="grid gap-5 sm:grid-cols-2">
                                    <div>
                                        <label class="mb-2 block text-xs font-medium uppercase tracking-wider text-[#2A2E38]/50">
                                            {$t('profile_phone')}
                                        </label>

                                        <input
                                            bind:value={phoneDraft}
                                            type="tel"
                                            placeholder="Telefonnummer"
                                            class="w-full border border-[#2A2E38]/15 bg-white p-4 text-sm outline-none transition focus:border-[#62AA97]"
                                        />
                                    </div>

                                    <div>
                                        <label class="mb-2 block text-xs font-medium uppercase tracking-wider text-[#2A2E38]/50">
                                            {$t('profile_location')}
                                        </label>

                                        <input
                                            bind:value={locationDraft}
                                            type="text"
                                            placeholder="Standort"
                                            class="w-full border border-[#2A2E38]/15 bg-white p-4 text-sm outline-none transition focus:border-[#62AA97]"
                                        />
                                    </div>

                                    <div class="flex flex-wrap gap-3 sm:col-span-2">
                                        <button
                                            type="button"
                                            onclick={saveContact}
                                            class="bg-[#62AA97] px-5 py-3 text-sm font-semibold text-[#2A2E38] transition hover:bg-[#A8B79E]"
                                        >
                                            Änderungen übernehmen
                                        </button>

                                        <button
                                            type="button"
                                            onclick={cancelContact}
                                            class="border border-[#2A2E38]/15 px-5 py-3 text-sm font-medium transition hover:bg-white"
                                        >
                                            Abbrechen
                                        </button>
                                    </div>
                                </div>
                            {:else}
                                <div class="grid gap-6 sm:grid-cols-2">

                                    {#if user.email}
                                        <div class="flex min-w-0 gap-4">
                                            <div class="flex h-12 w-12 shrink-0 items-center justify-center bg-[#A8B79E]/35 text-lg">
                                                ✉
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-xs uppercase tracking-wider text-[#2A2E38]/45">
                                                    {$t('profile_email')}
                                                </p>

                                                <p class="mt-2 break-all text-sm font-medium">
                                                    {user.email}
                                                </p>
                                            </div>
                                        </div>
                                    {/if}

                                    {#if displayedPhone}
                                        <div class="flex min-w-0 gap-4">
                                            <div class="flex h-12 w-12 shrink-0 items-center justify-center bg-[#8FB0C4]/30 text-lg">
                                                ☎
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-xs uppercase tracking-wider text-[#2A2E38]/45">
                                                    {$t('profile_phone')}
                                                </p>

                                                <p class="mt-2 break-words text-sm font-medium">
                                                    {displayedPhone}
                                                </p>
                                            </div>
                                        </div>
                                    {/if}

                                    {#if displayedLocation}
                                        <div class="flex min-w-0 gap-4">
                                            <div class="flex h-12 w-12 shrink-0 items-center justify-center bg-[#8FB0C4]/30 text-lg">
                                                📍
                                            </div>

                                            <div class="min-w-0">
                                                <p class="text-xs uppercase tracking-wider text-[#2A2E38]/45">
                                                    {$t('profile_location')}
                                                </p>

                                                <p class="mt-2 break-words text-sm font-medium">
                                                    {displayedLocation}
                                                </p>
                                            </div>
                                        </div>
                                    {/if}

                                    {#if !user.email && !displayedPhone && !displayedLocation}
                                        <p class="text-sm leading-7 text-[#2A2E38]/50">
                                            {$t('profile_no_contact')}
                                        </p>
                                    {/if}
                                </div>
                            {/if}
                        </div>
                    </section>
                </div>

                <!-- SIDEBAR -->
                <aside class="space-y-8">

                    <!-- NAVIGATION -->
                    <section class="bg-[#A8B79E] p-6 sm:p-7">
                        <p class="text-xs font-semibold uppercase tracking-[0.18em] text-[#2A2E38]/60">
                            NEXTJOB / NAVIGATION
                        </p>

                        <h2 class="mt-3 text-xl font-semibold tracking-tight">
                            {$t('profile_my_area')}
                        </h2>

                        <nav class="mt-6">
                            <a
                                href="/jobnehmer/hauptseite"
                                class="group flex items-center justify-between border-t border-[#2A2E38]/15 py-4 text-sm font-medium transition hover:pl-2"
                            >
                                <span>{$t('profile_discover_jobs')}</span>
                                <span class="transition group-hover:translate-x-1">↗</span>
                            </a>

                            <a
                                href="/saved"
                                class="group flex items-center justify-between border-t border-[#2A2E38]/15 py-4 text-sm font-medium transition hover:pl-2"
                            >
                                <span>{$t('worker_saved_jobs')}</span>
                                <span class="transition group-hover:translate-x-1">↗</span>
                            </a>
                        </nav>
                    </section>

                    <!-- INFORMATION -->
                    <section class="border border-[#2A2E38]/10 p-6">
                        <div class="flex items-center justify-between">
                            <span class="text-xs uppercase tracking-[0.2em] text-[#2A2E38]/45">
                                NEXTJOB
                            </span>

                            <span class="text-[#398875]">✳</span>
                        </div>

                        <p class="mt-5 text-lg font-medium leading-7 tracking-tight">
                            {$t('worker_role')}
                        </p>

                        <p class="mt-3 text-sm leading-7 text-[#2A2E38]/55">
                            {$t('profile_intro')}
                        </p>
                    </section>
                </aside>
            </div>

        {:else}
            <section class="border-l-4 border-[#62AA97] bg-white p-6">
                <h1 class="text-2xl font-semibold tracking-tight">
                    {$t('profile_unavailable')}
                </h1>

                <p class="mt-3 text-sm leading-7 text-[#2A2E38]/60">
                    {$t('profile_load_failed')}
                </p>
            </section>
        {/if}
    </main>
</div>