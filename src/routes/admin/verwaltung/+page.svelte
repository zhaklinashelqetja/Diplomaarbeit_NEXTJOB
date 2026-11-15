<script>
    let { data, form } = $props();

    let activeTab = $state('users');
    let searchUsers = $state('');
    let searchJobs = $state('');

    const users = $derived(
        data.users.filter((user) => {
            const query = searchUsers.toLowerCase().trim();

            const name = [
                user.first_name,
                user.last_name,
                user.name,
                user.username,
                user.email
            ]
                .filter(Boolean)
                .join(' ')
                .toLowerCase();

            return !query || name.includes(query);
        })
    );

    const jobs = $derived(
        data.jobs.filter((job) => {
            const query = searchJobs.toLowerCase().trim();

            const searchable = [
                job.title,
                job.description,
                job.location,
                job.category,
                job.category_name,
                job.status
            ]
                .filter(Boolean)
                .join(' ')
                .toLowerCase();

            return !query || searchable.includes(query);
        })
    );

    function userId(user) {
        return user.id ?? user.user_id ?? user._id;
    }

    function jobId(job) {
        return job.id ?? job.problem_id ?? job.job_id ?? job._id;
    }

    function userName(user) {
        const fullName = [user.first_name, user.last_name]
            .filter(Boolean)
            .join(' ');

        return (
            user.name ??
            user.full_name ??
            (fullName || user.username || 'Unbekannter Nutzer')
        );
    }

    function isUserActive(user) {
        if (typeof user.is_active === 'boolean') return user.is_active;
        if (typeof user.active === 'boolean') return user.active;
        if (typeof user.is_blocked === 'boolean') return !user.is_blocked;
        if (typeof user.is_suspended === 'boolean') return !user.is_suspended;

        return true;
    }

    function userRole(user) {
        return user.role ?? user.user_type ?? user.account_type ?? 'Nutzer';
    }

    function confirmDelete(message) {
        return confirm(message);
    }
</script>

<svelte:head>
    <title>Nutzer- und Auftragsverwaltung | NextJob</title>
    <meta
        name="description"
        content="NEXTJOB Admin-Verwaltung für Nutzerkonten und veröffentlichte Aufträge."
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10">
        <!-- Titel -->
        <section class="mb-8">
            <p
                class="text-xs font-bold uppercase tracking-[0.2em] text-[#529b88]"
            >
                Kontrolle und Sicherheit
            </p>

            <h1 class="mt-2 text-3xl font-extrabold sm:text-4xl">
                Admin-Verwaltung
            </h1>

            <p class="mt-3 max-w-2xl text-sm leading-6 text-[#2A2E38]/65 sm:text-base">
                Verwalte Nutzerkonten, kontrolliere veröffentlichte Aufträge
                und entferne Inhalte, die gegen die Plattformregeln verstoßen.
            </p>
        </section>

        <!-- Rückmeldungen -->
        {#if data.error}
            <div
                class="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
                role="alert"
            >
                {data.error}
            </div>
        {/if}

        {#if form?.actionError}
            <div
                class="mb-5 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-800"
                role="alert"
            >
                <p class="font-bold">Aktion fehlgeschlagen</p>
                <p class="mt-1">{form.actionError}</p>
            </div>
        {/if}

        {#if form?.success}
            <div
                class="mb-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800"
                role="status"
            >
                <p class="font-bold">Erfolgreich</p>
                <p class="mt-1">{form.message}</p>
            </div>
        {/if}

        <!-- Kennzahlen -->
        <section class="mb-8 grid gap-4 sm:grid-cols-3">
            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        Registrierte Nutzer
                    </p>
                    <span class="text-xl">👥</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">{data.users.length}</p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    Geladene Konten
                </p>
            </article>

            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        Veröffentlichte Aufträge
                    </p>
                    <span class="text-xl">📋</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">{data.jobs.length}</p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    Geladene Aufträge
                </p>
            </article>

            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        Gesperrte Nutzer
                    </p>
                    <span class="text-xl">🔒</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">
                    {data.users.filter((user) => !isUserActive(user)).length}
                </p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    Laut den gelieferten Kontodaten
                </p>
            </article>
        </section>

        <!-- Tabs -->
        <section class="overflow-hidden rounded-2xl border border-[#2A2E38]/10 bg-white shadow-sm">
            <div class="flex border-b border-[#2A2E38]/10 p-2 sm:p-3">
                <button
                    type="button"
                    class={`flex-1 rounded-xl px-3 py-3 text-sm font-bold transition sm:flex-none sm:px-6 ${
                        activeTab === 'users'
                            ? 'bg-[#2A2E38] text-white'
                            : 'text-[#2A2E38]/65 hover:bg-[#F5F1EE]'
                    }`}
                    onclick={() => (activeTab = 'users')}
                >
                    Nutzerverwaltung
                    <span class="ml-1 opacity-75">({data.users.length})</span>
                </button>

                <button
                    type="button"
                    class={`flex-1 rounded-xl px-3 py-3 text-sm font-bold transition sm:flex-none sm:px-6 ${
                        activeTab === 'jobs'
                            ? 'bg-[#2A2E38] text-white'
                            : 'text-[#2A2E38]/65 hover:bg-[#F5F1EE]'
                    }`}
                    onclick={() => (activeTab = 'jobs')}
                >
                    Auftragsverwaltung
                    <span class="ml-1 opacity-75">({data.jobs.length})</span>
                </button>
            </div>

            <!-- NUTZERVERWALTUNG -->
            {#if activeTab === 'users'}
                <div class="p-4 sm:p-6">
                    <div
                        class="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-end"
                    >
                        <div>
                            <h2 class="text-xl font-extrabold">
                                Nutzerkonten verwalten
                            </h2>
                            <p class="mt-1 text-sm text-[#2A2E38]/60">
                                Konten suchen, sperren, entsperren oder löschen.
                            </p>
                        </div>

                        <div class="w-full md:max-w-sm">
                            <label
                                for="user-search"
                                class="mb-2 block text-xs font-bold uppercase tracking-wide text-[#2A2E38]/55"
                            >
                                Nutzer suchen
                            </label>

                            <input
                                id="user-search"
                                bind:value={searchUsers}
                                placeholder="Name oder E-Mail eingeben ..."
                                class="w-full rounded-xl border border-[#2A2E38]/15 bg-[#F5F1EE] px-4 py-3 text-sm outline-none transition focus:border-[#62AA97] focus:ring-2 focus:ring-[#62AA97]/20"
                            />
                        </div>
                    </div>

                    {#if users.length > 0}
                        <div class="space-y-3">
                            {#each users as user}
                                <article
                                    class="rounded-xl border border-[#2A2E38]/10 p-4 transition hover:border-[#8FB0C4] sm:p-5"
                                >
                                    <div
                                        class="flex flex-col justify-between gap-4 lg:flex-row lg:items-center"
                                    >
                                        <div class="flex min-w-0 items-start gap-3">
                                            <div
                                                class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#A8B79E]/35 text-lg font-extrabold"
                                            >
                                                {userName(user).charAt(0).toUpperCase()}
                                            </div>

                                            <div class="min-w-0">
                                                <h3 class="break-words font-bold">
                                                    {userName(user)}
                                                </h3>

                                                <p class="mt-1 break-all text-sm text-[#2A2E38]/60">
                                                    {user.email ?? 'Keine E-Mail angegeben'}
                                                </p>

                                                <div
                                                    class="mt-2 flex flex-wrap items-center gap-2"
                                                >
                                                    <span
                                                        class="rounded-full bg-[#8FB0C4]/25 px-2.5 py-1 text-xs font-semibold"
                                                    >
                                                        {userRole(user)}
                                                    </span>

                                                    <span
                                                        class={`rounded-full px-2.5 py-1 text-xs font-bold ${
                                                            isUserActive(user)
                                                                ? 'bg-emerald-100 text-emerald-800'
                                                                : 'bg-red-100 text-red-800'
                                                        }`}
                                                    >
                                                        {isUserActive(user)
                                                            ? 'Aktiv'
                                                            : 'Gesperrt'}
                                                    </span>

                                                    <span class="text-xs text-[#2A2E38]/45">
                                                        ID: {userId(user) ?? '–'}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>

                                        <div
                                            class="flex flex-wrap gap-2 lg:justify-end"
                                        >
                                            <form
                                                method="POST"
                                                action="?/toggleUser"
                                                onsubmit={(event) => {
                                                    if (
                                                        !confirm(
                                                            isUserActive(user)
                                                                ? `Möchtest du ${userName(user)} wirklich sperren?`
                                                                : `Möchtest du ${userName(user)} wieder aktivieren?`
                                                        )
                                                    ) {
                                                        event.preventDefault();
                                                    }
                                                }}
                                            >
                                                <input
                                                    type="hidden"
                                                    name="userId"
                                                    value={userId(user) ?? ''}
                                                />
                                                <input
                                                    type="hidden"
                                                    name="isActive"
                                                    value={String(isUserActive(user))}
                                                />

                                                <button
                                                    type="submit"
                                                    disabled={!userId(user)}
                                                    class={`rounded-lg px-4 py-2.5 text-sm font-bold transition disabled:cursor-not-allowed disabled:opacity-40 ${
                                                        isUserActive(user)
                                                            ? 'bg-amber-100 text-amber-900 hover:bg-amber-200'
                                                            : 'bg-emerald-100 text-emerald-900 hover:bg-emerald-200'
                                                    }`}
                                                >
                                                    {isUserActive(user)
                                                        ? 'Sperren'
                                                        : 'Entsperren'}
                                                </button>
                                            </form>

                                            <form
                                                method="POST"
                                                action="?/deleteUser"
                                                onsubmit={(event) => {
                                                    if (
                                                        !confirm(
                                                            `Möchtest du das Konto von ${userName(user)} wirklich dauerhaft löschen? Diese Aktion kann nicht rückgängig gemacht werden.`
                                                        )
                                                    ) {
                                                        event.preventDefault();
                                                    }
                                                }}
                                            >
                                                <input
                                                    type="hidden"
                                                    name="userId"
                                                    value={userId(user) ?? ''}
                                                />

                                                <button
                                                    type="submit"
                                                    disabled={!userId(user)}
                                                    class="rounded-lg bg-red-600 px-4 py-2.5 text-sm font-bold text-white transition hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-40"
                                                >
                                                    Löschen
                                                </button>
                                            </form>
                                        </div>
                                    </div>
                                </article>
                            {/each}
                        </div>
                    {:else}
                        <div class="rounded-xl bg-[#F5F1EE] px-4 py-12 text-center">
                            <p class="text-3xl">👥</p>
                            <h3 class="mt-3 font-bold">
                                Keine Nutzer gefunden
                            </h3>
                            <p class="mt-1 text-sm text-[#2A2E38]/55">
                                Überprüfe deine Suche oder lade die Nutzerdaten
                                über die Backend-API.
                            </p>
                        </div>
                    {/if}
                </div>
            {/if}

            <!-- AUFTRAGSVERWALTUNG -->
            {#if activeTab === 'jobs'}
                <div class="p-4 sm:p-6">
                    <div
                        class="mb-6 flex flex-col justify-between gap-4 md:flex-row md:items-end"
                    >
                        <div>
                            <h2 class="text-xl font-extrabold">
                                Aufträge verwalten
                            </h2>
                            <p class="mt-1 text-sm text-[#2A2E38]/60">
                                Aufträge überprüfen, aktualisieren oder löschen.
                            </p>
                        </div>

                        <div class="w-full md:max-w-sm">
                            <label
                                for="job-search"
                                class="mb-2 block text-xs font-bold uppercase tracking-wide text-[#2A2E38]/55"
                            >
                                Auftrag suchen
                            </label>

                            <input
                                id="job-search"
                                bind:value={searchJobs}
                                placeholder="Titel, Kategorie oder Ort ..."
                                class="w-full rounded-xl border border-[#2A2E38]/15 bg-[#F5F1EE] px-4 py-3 text-sm outline-none transition focus:border-[#62AA97] focus:ring-2 focus:ring-[#62AA97]/20"
                            />
                        </div>
                    </div>

                    {#if jobs.length > 0}
                        <div class="space-y-4">
                            {#each jobs as job}
                                <article
                                    class="rounded-xl border border-[#2A2E38]/10 p-4 sm:p-5"
                                >
                                    <div
                                        class="mb-4 flex flex-wrap items-center justify-between gap-2"
                                    >
                                        <span
                                            class="rounded-full bg-[#8FB0C4]/25 px-3 py-1 text-xs font-bold"
                                        >
                                            {job.category_name ??
                                                job.category ??
                                                'Keine Kategorie'}
                                        </span>

                                        <span class="text-xs text-[#2A2E38]/50">
                                            ID: {jobId(job) ?? '–'}
                                        </span>
                                    </div>

                                    <form
                                        method="POST"
                                        action="?/updateJob"
                                        class="space-y-4"
                                        onsubmit={(event) => {
                                            if (
                                                !confirm(
                                                    'Möchtest du die Änderungen an diesem Auftrag speichern?'
                                                )
                                            ) {
                                                event.preventDefault();
                                            }
                                        }}
                                    >
                                        <input
                                            type="hidden"
                                            name="jobId"
                                            value={jobId(job) ?? ''}
                                        />

                                        <div>
                                            <label
                                                class="mb-2 block text-sm font-bold"
                                                for={`title-${jobId(job)}`}
                                            >
                                                Auftragstitel
                                            </label>

                                            <input
                                                id={`title-${jobId(job)}`}
                                                name="title"
                                                required
                                                value={job.title ?? job.name ?? ''}
                                                class="w-full rounded-xl border border-[#2A2E38]/15 px-4 py-3 text-sm outline-none transition focus:border-[#62AA97] focus:ring-2 focus:ring-[#62AA97]/20"
                                            />
                                        </div>

                                        <div>
                                            <label
                                                class="mb-2 block text-sm font-bold"
                                                for={`description-${jobId(job)}`}
                                            >
                                                Beschreibung
                                            </label>

                                            <textarea
                                                id={`description-${jobId(job)}`}
                                                name="description"
                                                required
                                                rows="3"
                                                class="w-full resize-y rounded-xl border border-[#2A2E38]/15 px-4 py-3 text-sm outline-none transition focus:border-[#62AA97] focus:ring-2 focus:ring-[#62AA97]/20"
                                            >{job.description ?? ''}</textarea>
                                        </div>

                                        <div class="grid gap-4 sm:grid-cols-2">
                                            <div>
                                                <label
                                                    class="mb-2 block text-sm font-bold"
                                                    for={`location-${jobId(job)}`}
                                                >
                                                    Standort
                                                </label>

                                                <input
                                                    id={`location-${jobId(job)}`}
                                                    readonly
                                                    value={job.location ?? job.city ?? 'Nicht angegeben'}
                                                    class="w-full rounded-xl border border-[#2A2E38]/10 bg-[#F5F1EE] px-4 py-3 text-sm text-[#2A2E38]/65"
                                                />
                                            </div>

                                            <div>
                                                <label
                                                    class="mb-2 block text-sm font-bold"
                                                    for={`status-${jobId(job)}`}
                                                >
                                                    Auftragsstatus
                                                </label>

                                                <select
                                                    id={`status-${jobId(job)}`}
                                                    name="status"
                                                    class="w-full rounded-xl border border-[#2A2E38]/15 bg-white px-4 py-3 text-sm outline-none focus:border-[#62AA97]"
                                                >
                                                    {#each ['open', 'in_progress', 'completed', 'closed', 'pending', 'rejected'] as status}
                                                        <option
                                                            value={status}
                                                            selected={(job.status ?? 'open') === status}
                                                        >
                                                            {({
                                                                open: 'Offen',
                                                                in_progress: 'In Bearbeitung',
                                                                completed: 'Abgeschlossen',
                                                                closed: 'Geschlossen',
                                                                pending: 'Ausstehend',
                                                                rejected: 'Abgelehnt'
                                                            })[status]}
                                                        </option>
                                                    {/each}
                                                </select>
                                            </div>
                                        </div>

                                        <div
                                            class="flex flex-wrap justify-end gap-2 border-t border-[#2A2E38]/10 pt-4"
                                        >
                                            <button
                                                type="submit"
                                                disabled={!jobId(job)}
                                                class="rounded-lg bg-[#2A2E38] px-4 py-2.5 text-sm font-bold text-white transition hover:bg-[#414653] disabled:opacity-40"
                                            >
                                                Änderungen speichern
                                            </button>
                                        </div>
                                    </form>

                                    <form
                                        method="POST"
                                        action="?/deleteJob"
                                        class="mt-2 flex justify-end"
                                        onsubmit={(event) => {
                                            if (
                                                !confirm(
                                                    `Möchtest du den Auftrag "${job.title ?? job.name ?? 'Ohne Titel'}" wirklich dauerhaft löschen?`
                                                )
                                            ) {
                                                event.preventDefault();
                                            }
                                        }}
                                    >
                                        <input
                                            type="hidden"
                                            name="jobId"
                                            value={jobId(job) ?? ''}
                                        />

                                        <button
                                            type="submit"
                                            disabled={!jobId(job)}
                                            class="rounded-lg border border-red-200 px-4 py-2.5 text-sm font-bold text-red-700 transition hover:bg-red-50 disabled:opacity-40"
                                        >
                                            Auftrag löschen
                                        </button>
                                    </form>
                                </article>
                            {/each}
                        </div>
                    {:else}
                        <div class="rounded-xl bg-[#F5F1EE] px-4 py-12 text-center">
                            <p class="text-3xl">📋</p>
                            <h3 class="mt-3 font-bold">
                                Keine Aufträge gefunden
                            </h3>
                            <p class="mt-1 text-sm text-[#2A2E38]/55">
                                Überprüfe deine Suche oder kontrolliere, ob
                                die Backend-API Aufträge zurückgibt.
                            </p>
                        </div>
                    {/if}
                </div>
            {/if}
        </section>

        <footer
            class="mt-8 border-t border-[#2A2E38]/10 pt-5 text-xs text-[#2A2E38]/50"
        >
            NEXTJOB · Admin-Verwaltung · Nutzerkonten und Aufträge
        </footer>
    </main>
</div>