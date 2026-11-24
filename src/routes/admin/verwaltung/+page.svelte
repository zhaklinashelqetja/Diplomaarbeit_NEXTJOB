
<script>
    import * as m from '$lib/paraglide/messages.js';

    let { data, form } = $props();

    let activeTab = $state('users');
    let searchUsers = $state('');
    let searchJobs = $state('');

    // Daten sicher laden, auch wenn die API nichts zurückgibt
    const allUsers = $derived(
        Array.isArray(data?.users) ? data.users : []
    );

    const allJobs = $derived(
        Array.isArray(data?.jobs) ? data.jobs : []
    );

    // Nutzer filtern
    const users = $derived(
        allUsers.filter((user) => {
            const query = searchUsers.toLowerCase().trim();

            const searchable = [
                user.first_name,
                user.last_name,
                user.name,
                user.full_name,
                user.username,
                user.email
            ]
                .filter(Boolean)
                .join(' ')
                .toLowerCase();

            return !query || searchable.includes(query);
        })
    );

    // Aufträge filtern
    const jobs = $derived(
        allJobs.filter((job) => {
            const query = searchJobs.toLowerCase().trim();

            const searchable = [
                job.title,
                job.name,
                job.description,
                job.location,
                job.city,
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

    // Nutzer-ID ermitteln
    function userId(user) {
        return user.id ?? user.user_id ?? user._id ?? null;
    }

    // Auftrags-ID ermitteln
    function jobId(job) {
        return job.id ?? job.problem_id ?? job.job_id ?? job._id ?? null;
    }

    // Nutzernamen ermitteln
    function userName(user) {
        const fullName = [
            user.first_name,
            user.last_name
        ]
            .filter(Boolean)
            .join(' ');

        return (
            user.name ??
            user.full_name ??
            fullName ??
            user.username ??
            m.admin_manage_unknown_user()
        );
    }

    // Nutzerstatus ermitteln
    function isUserActive(user) {
        if (typeof user.is_active === 'boolean') {
            return user.is_active;
        }

        if (typeof user.active === 'boolean') {
            return user.active;
        }

        if (typeof user.is_blocked === 'boolean') {
            return !user.is_blocked;
        }

        if (typeof user.is_suspended === 'boolean') {
            return !user.is_suspended;
        }

        return true;
    }

    // Nutzerrolle ermitteln
    function userRole(user) {
        const role =
            user.role ??
            user.user_type ??
            user.account_type ??
            m.admin_manage_role_user();

        const roles = {
            jobgeber: m.admin_manage_role_employer(),
            jobnehmer: m.admin_manage_role_worker(),
            admin: m.admin_manage_role_admin(),
            administrator: m.admin_manage_role_admin()
        };

        return roles[String(role).toLowerCase()] ?? role;
    }

    // Lösch- und Änderungsbestätigung
    function confirmAction(message) {
        return window.confirm(message);
    }
</script>

<svelte:head>
    <title>{m.admin_manage_page_title()} | NextJob</title>
    <meta
        name="description"
        content={m.admin_manage_meta_description()}
    />
</svelte:head>

<div class="min-h-screen bg-[#F5F1EE] text-[#2A2E38]">

    <main class="mx-auto max-w-7xl px-4 py-8 sm:px-6 sm:py-10">
        <!-- Titel -->
        <section class="mb-8">
            <p
                class="text-xs font-bold uppercase tracking-[0.2em] text-[#529b88]"
            >
                {m.admin_manage_security()}
            </p>

            <h1 class="mt-2 text-3xl font-extrabold sm:text-4xl">
                {m.admin_manage_title()}
            </h1>

            <p class="mt-3 max-w-2xl text-sm leading-6 text-[#2A2E38]/65 sm:text-base">
                {m.admin_manage_description()}
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
                <p class="font-bold">{m.admin_manage_action_failed()}</p>
                <p class="mt-1">{form.actionError}</p>
            </div>
        {/if}

        {#if form?.success}
            <div
                class="mb-5 rounded-xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-800"
                role="status"
            >
                <p class="font-bold">{m.admin_manage_success()}</p>
                <p class="mt-1">{form.message}</p>
            </div>
        {/if}

        <!-- Kennzahlen -->
        <section class="mb-8 grid gap-4 sm:grid-cols-3">
            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        {m.admin_manage_registered_users()}
                    </p>
                    <span class="text-xl">👥</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">{data.users.length}</p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    {m.admin_manage_loaded_accounts()}
                </p>
            </article>

            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        {m.admin_manage_published_jobs()}
                    </p>
                    <span class="text-xl">📋</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">{data.jobs.length}</p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    {m.admin_manage_loaded_jobs()}
                </p>
            </article>

            <article class="rounded-2xl border border-[#2A2E38]/10 bg-white p-5 shadow-sm">
                <div class="flex items-center justify-between gap-3">
                    <p class="text-sm font-semibold text-[#2A2E38]/60">
                        {m.admin_manage_blocked_users()}
                    </p>
                    <span class="text-xl">🔒</span>
                </div>
                <p class="mt-3 text-3xl font-extrabold">
                    {data.users.filter((user) => !isUserActive(user)).length}
                </p>
                <p class="mt-1 text-xs text-[#2A2E38]/50">
                    {m.admin_manage_account_data_note()}
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
                    {m.admin_manage_users_tab()}
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
                    {m.admin_manage_jobs_tab()}
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
                                {m.admin_manage_user_accounts()}
                            </h2>
                            <p class="mt-1 text-sm text-[#2A2E38]/60">
                                {m.admin_manage_users_description()}
                            </p>
                        </div>

                        <div class="w-full md:max-w-sm">
                            <label
                                for="user-search"
                                class="mb-2 block text-xs font-bold uppercase tracking-wide text-[#2A2E38]/55"
                            >
                                {m.admin_manage_search_user()}
                            </label>

                            <input
                                id="user-search"
                                bind:value={searchUsers}
                                placeholder={m.admin_manage_user_placeholder()}
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
                                                    {user.email ?? m.admin_manage_no_email()}
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
                                                            ? m.admin_manage_active()
                                                            : m.admin_manage_blocked()}
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
                                                                ? m.admin_manage_confirm_block({ name: userName(user) })
                                                                : m.admin_manage_confirm_unblock({ name: userName(user) })
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
                                                        ? m.admin_manage_block()
                                                        : m.admin_manage_unblock()}
                                                </button>
                                            </form>

                                            <form
                                                method="POST"
                                                action="?/deleteUser"
                                                onsubmit={(event) => {
                                                    if (
                                                        !confirm(
                                                            m.admin_manage_confirm_delete_user({ name: userName(user) })
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
                                                    {m.admin_manage_delete()}
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
                                {m.admin_manage_no_users()}
                            </h3>
                            <p class="mt-1 text-sm text-[#2A2E38]/55">
                                {m.admin_manage_no_users_description()}
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
                                {m.admin_manage_jobs_title()}
                            </h2>
                            <p class="mt-1 text-sm text-[#2A2E38]/60">
                                {m.admin_manage_jobs_description()}
                            </p>
                        </div>

                        <div class="w-full md:max-w-sm">
                            <label
                                for="job-search"
                                class="mb-2 block text-xs font-bold uppercase tracking-wide text-[#2A2E38]/55"
                            >
                                {m.admin_manage_search_job()}
                            </label>

                            <input
                                id="job-search"
                                bind:value={searchJobs}
                                placeholder={m.admin_manage_job_placeholder()}
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
                                                m.admin_manage_no_category()}
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
                                                    m.admin_manage_confirm_save()
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
                                                {m.admin_manage_job_title()}
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
                                                {m.admin_manage_job_description()}
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
                                                    {m.admin_manage_location()}
                                                </label>

                                                <input
                                                    id={`location-${jobId(job)}`}
                                                    readonly
                                                    value={job.location ?? job.city ?? m.admin_manage_not_specified()}
                                                    class="w-full rounded-xl border border-[#2A2E38]/10 bg-[#F5F1EE] px-4 py-3 text-sm text-[#2A2E38]/65"
                                                />
                                            </div>

                                            <div>
                                                <label
                                                    class="mb-2 block text-sm font-bold"
                                                    for={`status-${jobId(job)}`}
                                                >
                                                    {m.admin_manage_job_status()}
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
                                                                open: m.admin_manage_status_open(),
                                                                in_progress: m.admin_manage_status_progress(),
                                                                completed: m.admin_manage_status_completed(),
                                                                closed: m.admin_manage_status_closed(),
                                                                pending: m.admin_manage_status_pending(),
                                                                rejected: m.admin_manage_status_rejected()
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
                                                {m.admin_manage_save_changes()}
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
                                                    m.admin_manage_confirm_delete_job({
                                                        title: job.title ?? job.name ?? m.admin_manage_untitled()
                                                    })
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
                                            {m.admin_manage_delete_job()}
                                        </button>
                                    </form>
                                </article>
                            {/each}
                        </div>
                    {:else}
                        <div class="rounded-xl bg-[#F5F1EE] px-4 py-12 text-center">
                            <p class="text-3xl">📋</p>
                            <h3 class="mt-3 font-bold">
                                {m.admin_manage_no_jobs()}
                            </h3>
                            <p class="mt-1 text-sm text-[#2A2E38]/55">
                                {m.admin_manage_no_jobs_description()}
                            </p>
                        </div>
                    {/if}
                </div>
            {/if}
        </section>

        <footer
            class="mt-8 border-t border-[#2A2E38]/10 pt-5 text-xs text-[#2A2E38]/50"
        >
            {m.admin_manage_footer()}
        </footer>
    </main>
</div>
