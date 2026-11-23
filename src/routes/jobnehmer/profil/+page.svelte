<script>
    import { t } from '$lib/i18n.js';
    import { API_URL } from '$lib/api.js';

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
                .map(skill =>
                    typeof skill === 'string'
                        ? skill
                        : skill?.name ?? skill?.category_name
                )
                .filter(Boolean);
        }

        if (typeof value === 'string' && value.trim()) {
            return value.split(',').map(s => s.trim()).filter(Boolean);
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

    // FOLLOWERS & FOLLOWING
    let showFollowers = $state(false);
    let showFollowing = $state(false);

    let followers = $derived(
        Array.isArray(user?.followers) ? user.followers : []
    );

    let following = $derived(
        Array.isArray(user?.following) ? user.following : []
    );

    let followersCount = $derived(
        user?.followers_count ?? user?.follower_count ?? followers.length
    );

    let followingCount = $derived(
        user?.following_count ?? user?.follow_count ?? following.length
    );

    // DATABASE DATA
    let categoriesList = $state([]);
    let neighborhoodsList = $state([]);
    let selectedCategoryIds = $state([]);
    let initializedUserKey = $state('');

    // HELPERS
    function normalizeText(value) {
        return String(value ?? '')
            .normalize('NFD')
            .replace(/[\u0300-\u036f]/g, '')
            .trim()
            .toLowerCase();
    }

    function extractList(data) {
        if (Array.isArray(data)) return data;

        if (Array.isArray(data?.categories)) return data.categories;
        if (Array.isArray(data?.neighborhoods)) return data.neighborhoods;
        if (Array.isArray(data?.data)) return data.data;
        if (Array.isArray(data?.items)) return data.items;

        return [];
    }

    function getCategoryName(category) {
        return category?.name
            ?? category?.category_name
            ?? category?.title
            ?? '';
    }

    function getCategoryId(category) {
        return category?.category_id
            ?? category?.id
            ?? category?.id_category;
    }

    function getNeighborhoodName(item) {
        return item?.name
            ?? item?.neighborhood_name
            ?? item?.title
            ?? '';
    }

    function getNeighborhoodId(item) {
        return item?.neighborhood_id
            ?? item?.id
            ?? item?.id_neighborhood;
    }

    async function apiRequest(path, options = {}) {
        const token = localStorage.getItem('token');

        if (!token) {
            throw new Error('Bitte melde dich erneut an.');
        }

        const response = await fetch(`${API_URL}/api${path}`, {
            ...options,
            headers: {
                Authorization: `Bearer ${token}`,
                ...(options.headers || {})
            }
        });

        const result = await response.json().catch(() => ({}));

        if (!response.ok) {
            throw new Error(
                result.message ||
                result.error ||
                'Speichern fehlgeschlagen.'
            );
        }

        return result;
    }

    // INITIALIZATION
    $effect(() => {
        if (!user) return;

        const userKey = String(user.id ?? user.email ?? 'default');

        if (initializedUserKey === userKey) return;

        initializedUserKey = userKey;

        (async () => {
            try {
                const [catResponse, neighborhoodResponse] =
                    await Promise.all([
                        fetch(`${API_URL}/api/categories`),
                        fetch(`${API_URL}/api/neighborhoods`)
                    ]);

                if (catResponse.ok) {
                    const catData = await catResponse.json();
                    categoriesList = extractList(catData);
                }

                if (neighborhoodResponse.ok) {
                    const neighborhoodData =
                        await neighborhoodResponse.json();

                    neighborhoodsList = extractList(neighborhoodData);
                }
            } catch (error) {
                console.error(
                    'Kategorien oder Standorte konnten nicht geladen werden:',
                    error
                );
            }

            displayedBio = bio;
            displayedSkills = skills;
            displayedPhone = user.phone ?? '';

            displayedLocation =
                location ||
                user.neighborhood_name ||
                user.neighborhood ||
                '';

            profileImage =
                user.avatar_path ||
                user.profile_image ||
                user.profile_picture ||
                user.avatar ||
                user.image ||
                '';

            bioDraft = displayedBio;
            skillsDraft = displayedSkills.join(', ');
            phoneDraft = displayedPhone;
            locationDraft = displayedLocation;
        })();
    });

    // BIO
    async function saveBio() {
        const value = bioDraft.trim();

        try {
            await apiRequest('/workers/me', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ bio: value })
            });

            displayedBio = value;
            editingBio = false;
        } catch (error) {
            alert(
                error.message ||
                'Die Beschreibung konnte nicht gespeichert werden.'
            );
        }
    }

    function startEditingBio() {
        bioDraft = displayedBio;
        editingBio = true;
    }

    function cancelBio() {
        bioDraft = displayedBio;
        editingBio = false;
    }

    // SKILLS: DATABASE CATEGORY IDs
    function startEditingSkills() {
        selectedCategoryIds = displayedSkills
            .map(skill => {
                if (typeof skill === 'object') {
                    return Number(getCategoryId(skill));
                }

                const category = categoriesList.find(item =>
                    normalizeText(getCategoryName(item)) ===
                    normalizeText(skill)
                );

                return category
                    ? Number(getCategoryId(category))
                    : null;
            })
            .filter(id => id != null);

        editingSkills = true;
    }

    async function saveSkills() {
        if (!categoriesList.length) {
            alert(
                'Die Kategorien aus der Datenbank konnten nicht geladen werden. Bitte lade die Seite erneut.'
            );
            return;
        }

        if (!selectedCategoryIds.length) {
            alert('Bitte wähle mindestens eine Kategorie aus.');
            return;
        }

        try {
            await apiRequest('/workers/me/categories', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    category_ids: selectedCategoryIds.map(Number)
                })
            });

            displayedSkills = categoriesList.filter(category =>
                selectedCategoryIds.includes(
                    Number(getCategoryId(category))
                )
            );

            skillsDraft = displayedSkills
                .map(getCategoryName)
                .join(', ');

            editingSkills = false;

        } catch (error) {
            alert(
                error.message ||
                'Skills konnten nicht in der Datenbank gespeichert werden.'
            );
        }
    }

    function cancelSkills() {
        selectedCategoryIds = [];
        editingSkills = false;
    }

    function toggleSkill(categoryId) {
        const id = Number(categoryId);

        if (selectedCategoryIds.includes(id)) {
            selectedCategoryIds = selectedCategoryIds.filter(
                selectedId => selectedId !== id
            );
        } else {
            selectedCategoryIds = [...selectedCategoryIds, id];
        }
    }

    // CONTACT
    function startEditingContact() {
        phoneDraft = displayedPhone;
        locationDraft = displayedLocation;
        editingContact = true;
    }

    async function saveContact() {
        const phone = phoneDraft.trim();
        const place = locationDraft.trim();

        const neighborhood = neighborhoodsList.find(item =>
            normalizeText(getNeighborhoodName(item)) ===
            normalizeText(place)
        );

        if (place && !neighborhood) {
            const available = neighborhoodsList
                .map(getNeighborhoodName)
                .filter(Boolean);

            alert(
                `Standort nicht gefunden.\n\nVerfügbare Standorte: ${available.join(', ')}`
            );

            return;
        }

        const payload = { phone };

        if (neighborhood) {
            payload.neighborhood_id = Number(
                getNeighborhoodId(neighborhood)
            );
        }

        try {
            await apiRequest('/users/me', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            displayedPhone = phone;

            displayedLocation = neighborhood
                ? getNeighborhoodName(neighborhood)
                : '';

            editingContact = false;

        } catch (error) {
            alert(
                error.message ||
                'Kontaktinformationen konnten nicht gespeichert werden.'
            );
        }
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

    async function handleImageChange(event) {
        const file = event.currentTarget.files?.[0];

        if (!file) return;

        if (!file.type.startsWith('image/')) {
            alert('Bitte wähle eine Bilddatei aus.');
            return;
        }

        const formData = new FormData();
        formData.append('avatar', file);

        try {
            const result = await apiRequest('/users/me/avatar', {
                method: 'POST',
                body: formData
            });

            profileImage = result.avatar_path || '';

            if (
                profileImage &&
                !profileImage.startsWith('http')
            ) {
                profileImage = `${API_URL}${profileImage}`;
            }

        } catch (error) {
            alert(
                error.message ||
                'Das Profilbild konnte nicht gespeichert werden.'
            );
        } finally {
            event.currentTarget.value = '';
        }
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

                        <!-- FOLLOWERS & FOLLOWING -->
                        <div class="mt-6 flex flex-wrap items-center gap-8">

                            <!-- FOLLOWERS -->
                            <button
                                type="button"
                                onclick={() => {
                                    showFollowers = !showFollowers;
                                    showFollowing = false;
                                }}
                                class="group text-left transition"
                            >
                                <div class="flex items-baseline gap-2">
                                    <span class="text-2xl font-semibold text-white">
                                        {followersCount}
                                    </span>

                                    <span class="text-sm text-white/60 transition group-hover:text-[#A8B79E]">
                                        Followers
                                    </span>
                                </div>

                                <div class="mt-1 h-px w-full bg-white/20 transition group-hover:bg-[#62AA97]"></div>
                            </button>

                            <!-- FOLLOWING -->
                            <button
                                type="button"
                                onclick={() => {
                                    showFollowing = !showFollowing;
                                    showFollowers = false;
                                }}
                                class="group text-left transition"
                            >
                                <div class="flex items-baseline gap-2">
                                    <span class="text-2xl font-semibold text-white">
                                        {followingCount}
                                    </span>

                                    <span class="text-sm text-white/60 transition group-hover:text-[#A8B79E]">
                                        Following
                                    </span>
                                </div>

                                <div class="mt-1 h-px w-full bg-white/20 transition group-hover:bg-[#62AA97]"></div>
                            </button>

                        </div>

                        <!-- FOLLOWERS LIST -->
                        {#if showFollowers}
                            <div class="mt-5 max-w-md border border-white/10 bg-white/5 p-5">
                                <div class="mb-4 flex items-center justify-between">
                                    <h3 class="text-sm font-semibold text-white">
                                        Followers
                                    </h3>

                                    <button
                                        type="button"
                                        onclick={() => showFollowers = false}
                                        class="text-white/50 transition hover:text-white"
                                        aria-label="Close followers"
                                    >
                                        ✕
                                    </button>
                                </div>

                                {#if followers.length > 0}
                                    <div class="space-y-3">
                                        {#each followers as follower, index (`follower-${follower.id ?? index}`)}
                                            <div class="flex items-center gap-3 border-t border-white/10 pt-3">
                                                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#A8B79E] text-sm font-semibold text-[#2A2E38]">
                                                    {(follower.first_name?.charAt(0) ?? '')}{(follower.last_name?.charAt(0) ?? '')}
                                                </div>

                                                <div class="min-w-0">
                                                    <p class="break-words text-sm font-medium text-white">
                                                        {follower.first_name ?? ''} {follower.last_name ?? ''}
                                                    </p>
                                                </div>
                                            </div>
                                        {/each}
                                    </div>
                                {:else}
                                    <p class="text-sm leading-6 text-white/50">
                                        Noch keine Follower verfügbar.
                                    </p>
                                {/if}
                            </div>
                        {/if}

                        <!-- FOLLOWING LIST -->
                        {#if showFollowing}
                            <div class="mt-5 max-w-md border border-white/10 bg-white/5 p-5">
                                <div class="mb-4 flex items-center justify-between">
                                    <h3 class="text-sm font-semibold text-white">
                                        Following
                                    </h3>

                                    <button
                                        type="button"
                                        onclick={() => showFollowing = false}
                                        class="text-white/50 transition hover:text-white"
                                        aria-label="Close following"
                                    >
                                        ✕
                                    </button>
                                </div>

                                {#if following.length > 0}
                                    <div class="space-y-3">
                                        {#each following as followedUser, index (`following-${followedUser.id ?? index}`)}
                                            <div class="flex items-center gap-3 border-t border-white/10 pt-3">
                                                <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-[#8FB0C4] text-sm font-semibold text-[#2A2E38]">
                                                    {(followedUser.first_name?.charAt(0) ?? '')}{(followedUser.last_name?.charAt(0) ?? '')}
                                                </div>

                                                <div class="min-w-0">
                                                    <p class="break-words text-sm font-medium text-white">
                                                        {followedUser.first_name ?? ''} {followedUser.last_name ?? ''}
                                                    </p>
                                                </div>
                                            </div>
                                        {/each}
                                    </div>
                                {:else}
                                    <p class="text-sm leading-6 text-white/50">
                                        Du folgst noch niemandem.
                                    </p>
                                {/if}
                            </div>
                        {/if}

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
            <div class="mt-10">

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
                                <div class="space-y-5">

                                    {#if categoriesList.length > 0}
                                        <div class="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
                                            {#each categoriesList as category, index (`category-${getCategoryId(category) ?? index}`)}
                                                <button
                                                    type="button"
                                                    onclick={() => toggleSkill(getCategoryId(category))}
                                                    class={`flex items-center justify-between gap-3 border p-4 text-left text-sm transition ${
                                                        selectedCategoryIds.includes(Number(getCategoryId(category)))
                                                            ? 'border-[#62AA97] bg-[#A8B79E]/25'
                                                            : 'border-[#2A2E38]/10 bg-white hover:border-[#62AA97]'
                                                    }`}
                                                >
                                                    <span class="font-medium">
                                                        {getCategoryName(category)}
                                                    </span>

                                                    <span class={`flex h-5 w-5 shrink-0 items-center justify-center border ${
                                                        selectedCategoryIds.includes(Number(getCategoryId(category)))
                                                            ? 'border-[#398875] bg-[#62AA97] text-[#2A2E38]'
                                                            : 'border-[#2A2E38]/25'
                                                    }`}>
                                                        {#if selectedCategoryIds.includes(Number(getCategoryId(category)))}
                                                            ✓
                                                        {/if}
                                                    </span>
                                                </button>
                                            {/each}
                                        </div>
                                    {:else}
                                        <p class="text-sm text-red-600">
                                            Kategorien konnten nicht geladen werden.
                                        </p>
                                    {/if}

                                    <p class="text-xs leading-5 text-[#2A2E38]/50">
                                        Wähle alle Kategorien aus, die zu deinen Fähigkeiten passen.
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
                                        {#each displayedSkills as skill, index (`${getCategoryName(skill) || skill}-${index}`)}
                                            <span
                                                class="border border-[#2A2E38]/10 bg-white px-4 py-3 text-sm font-medium transition hover:border-[#62AA97] hover:bg-[#A8B79E]/20"
                                            >
                                                {typeof skill === 'object'
                                                    ? getCategoryName(skill)
                                                    : skill}
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