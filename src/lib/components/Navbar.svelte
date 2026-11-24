<script>
    import { goto } from '$app/navigation';
    import { API_URL } from '$lib/api.js';
    import { resolve } from '$app/paths';
    import { page } from '$app/state';
    import * as m from '$lib/paraglide/messages.js';
    import { getLocale, setLocale } from '$lib/paraglide/runtime.js';
    import { isLoggedIn, currentUser, logout } from '$lib/auth.js';

    import {
        House, BriefcaseBusiness, MessageCircle, Bell,
        UserRound, Menu, X, ChevronDown, ArrowUpRight,
        LogOut, Search, Info
    } from '@lucide/svelte';

    let menuOpen = $state(false);
    let profileOpen = $state(false);
    let searchQuery = $state('');
    let searchCategory = $state('all');
    let searchOpen = $state(false);
    let selectedLocale = $state(getLocale());

    let accountType = $derived($currentUser?.account_type);

    let emailUnverified = $derived(
        $isLoggedIn &&
        $currentUser &&
        $currentUser.is_verified === false
    );

    let profileName = $derived(
        `${$currentUser?.first_name ?? ''} ${$currentUser?.last_name ?? ''}`.trim() ||
        $currentUser?.name ||
        $currentUser?.username ||
        $currentUser?.email?.split('@')[0] ||
        'NextJob'
    );

    let profileInitial = $derived(
        profileName.charAt(0).toUpperCase()
    );

    let profileAvatar = $derived.by(() => {
        const image = $currentUser?.avatar_path ||
            $currentUser?.profile_image ||
            $currentUser?.profile_picture ||
            $currentUser?.avatar || '';

        if (!image) return '';

        try {
            return new URL(image, API_URL).href;
        } catch {
            return '';
        }
    });

    let failedAvatar = $state('');

    function closeMenu() {
        menuOpen = false;
        profileOpen = false;
    }

    function handleLogout() {
        logout();
        closeMenu();
        goto(resolve('/'));
    }

    function isActive(path) {
        return page.url.pathname === resolve(path);
    }

    function submitSearch(event) {
        event.preventDefault();

        const query = searchQuery.trim();
        if (!query) return;

        const params = new URLSearchParams({
            q: query,
            type: searchCategory
        });

        searchOpen = false;
        goto(`${resolve('/suche')}?${params.toString()}`);
    }

    function selectCategory(category) {
        searchCategory = category;
    }

    function changeLanguage(locale) {
        if (selectedLocale === locale) return;

        setLocale(locale);
        selectedLocale = locale;
        searchOpen = false;
    }
</script>

<svelte:head>
    <meta name="theme-color" content="#F5F1EE" />
</svelte:head>

<nav class="nextjob-nav">
    <div class="nav-container">

        <!-- Logo -->
        <a
            href={resolve('/')}
            class="brand"
            onclick={closeMenu}
            aria-label={m.nav_home_aria()}
        >
            <img
                src="/images/nextjob-logo.png"
                alt="NextJob Logo"
                class="brand-logo"
            />
            <span class="brand-name">NEXTJOB</span>
        </a>

        <!-- Suche -->
        <div class="search-wrapper">
            <form
                class="nav-search"
                role="search"
                onsubmit={submitSearch}
            >
                <Search
                    size={19}
                    strokeWidth={1.8}
                    class="search-icon"
                    aria-hidden="true"
                />

                <input
                    type="search"
                    bind:value={searchQuery}
                    onfocus={() => (searchOpen = true)}
                    placeholder={m.search_jobs()}
                    aria-label={m.search_jobs()}
                />

                {#if searchQuery}
                    <button
                        type="button"
                        class="search-clear"
                        onclick={() => (searchQuery = '')}
                        aria-label={m.nav_search_clear()}
                    >
                        <X size={16} />
                    </button>
                {/if}

                <button
                    type="submit"
                    class="search-submit"
                    disabled={!searchQuery.trim()}
                    aria-label={m.nav_search_submit()}
                >
                    <ArrowUpRight size={19} />
                </button>
            </form>

            {#if searchOpen}
                <div class="search-panel">
                    <div class="search-panel-header">
                        <span>{m.nav_search_filter_heading()}</span>
                        <button
                            type="button"
                            onclick={() => (searchOpen = false)}
                            aria-label={m.nav_search_filter_close()}
                        >
                            <X size={15} />
                        </button>
                    </div>

                    <div class="search-filters">
                        <button
                            type="button"
                            class:chosen={searchCategory === 'all'}
                            onclick={() => selectCategory('all')}
                        >
                            {m.search_all()}
                        </button>

                        <button
                            type="button"
                            class:chosen={searchCategory === 'jobs'}
                            onclick={() => selectCategory('jobs')}
                        >
                            <BriefcaseBusiness size={15} />
                            {m.nav_jobs_short()}
                        </button>

                        <button
                            type="button"
                            class:chosen={searchCategory === 'users'}
                            onclick={() => selectCategory('users')}
                        >
                            <UserRound size={15} />
                            {m.search_users()}
                        </button>
                    </div>

                    <p class="search-help">
                        {m.nav_search_help()}
                    </p>
                </div>
            {/if}
        </div>

        <!-- Desktop Navigation -->
        <div class="desktop-navigation">
            <a
                href={resolve('/landing')}
                class="nav-icon-link how-link"
                class:active={isActive('/landing')}
                onclick={closeMenu}
            >
                <Info size={21} strokeWidth={1.7} />
                <span>{m.nav_how_nextjob_works()}</span>
            </a>

            {#if $isLoggedIn}
                <a
                    href={resolve('/')}
                    class="nav-icon-link"
                    class:active={isActive('/')}
                    aria-current={isActive('/') ? 'page' : undefined}
                >
                    <House size={21} strokeWidth={1.7} />
                    <span>{m.nav_start()}</span>
                </a>

                <a
                    href={resolve('/jobs')}
                    class="nav-icon-link"
                    class:active={isActive('/jobs')}
                    aria-current={isActive('/jobs') ? 'page' : undefined}
                >
                    <BriefcaseBusiness size={21} strokeWidth={1.7} />
                    <span>{m.nav_jobs_short()}</span>
                </a>

                {#if accountType === 'jobnehmer'}
                    <a
                        href={resolve('/jobnehmer/profil')}
                        class="nav-icon-link"
                        class:active={isActive('/jobnehmer/profil')}
                    >
                        <UserRound size={21} strokeWidth={1.7} />
                        <span>{m.nav_my_profile()}</span>
                    </a>
                {/if}

                <a
                    href={resolve('/chat')}
                    class="nav-icon-link"
                    class:active={isActive('/chat')}
                >
                    <MessageCircle size={21} strokeWidth={1.7} />
                    <span>{m.nav_messages()}</span>
                </a>

                <a
                    href={resolve('/benachrichtigungen')}
                    class="nav-icon-link"
                    class:active={isActive('/benachrichtigungen')}
                >
                    <Bell size={21} strokeWidth={1.7} />
                    <span>{m.nav_notifications()}</span>
                </a>
            {:else}
                <a
                    href={resolve('/')}
                    class="public-link"
                    class:active={isActive('/')}
                >
                    {m.nav_start()}
                </a>

                <a
                    href={resolve('/jobs')}
                    class="public-link"
                    class:active={isActive('/jobs')}
                >
                    {m.nav_jobs_services()}
                </a>
            {/if}
        </div>

        <!-- Desktop Actions -->
        <div class="desktop-actions">

            <!-- Sprachwechsel -->
            <div class="language-switch" aria-label={m.nav_language_label()}>
                <button
                    type="button"
                    class:active={selectedLocale === 'de'}
                    aria-pressed={selectedLocale === 'de'}
                    onclick={() => changeLanguage('de')}
                >
                    DE
                </button>

                <span class="language-separator">|</span>

                <button
                    type="button"
                    class:active={selectedLocale === 'sq'}
                    aria-pressed={selectedLocale === 'sq'}
                    onclick={() => changeLanguage('sq')}
                >
                    SQ
                </button>

                <span class="language-separator">|</span>

                <button
                    type="button"
                    class:active={selectedLocale === 'en'}
                    aria-pressed={selectedLocale === 'en'}
                    onclick={() => changeLanguage('en')}
                >
                    EN
                </button>
            </div>

            {#if $isLoggedIn}
                <div class="profile-container">
                    <button
                        type="button"
                        class="profile-trigger"
                        onclick={() => (profileOpen = !profileOpen)}
                        aria-expanded={profileOpen}
                        aria-label={m.nav_profile_menu()}
                    >
                        <span class="avatar">
                            {#if profileAvatar && failedAvatar !== profileAvatar}
                                <img
                                    src={profileAvatar}
                                    alt=""
                                    onerror={() => failedAvatar = profileAvatar}
                                />
                            {:else}
                                {profileInitial}
                            {/if}
                        </span>

                        <ChevronDown size={15} strokeWidth={1.7} />
                    </button>

                    {#if profileOpen}
                        <div class="profile-dropdown">
                            <div class="profile-info">
                                <p class="profile-name">
                                    {profileName}
                                </p>
                                <p class="profile-email">
                                    {$currentUser?.email || ''}
                                </p>
                            </div>

                            {#if accountType === 'jobnehmer'}
                                <a
                                    href={resolve('/jobnehmer/profil')}
                                    onclick={closeMenu}
                                    class="dropdown-link"
                                >
                                    <UserRound size={17} />
                                    {m.nav_my_profile()}
                                </a>
                            {/if}

                            <button
                                type="button"
                                class="dropdown-link logout-link"
                                onclick={handleLogout}
                            >
                                <LogOut size={17} />
                                {m.nav_logout()}
                            </button>
                        </div>
                    {/if}
                </div>
            {:else}
                <a
                    href={resolve('/auth/login')}
                    class="login-link"
                >
                    {m.nav_login()}
                </a>

                <a
                    href={resolve('/auth/register')}
                    class="register-button"
                >
                    {m.nav_register()}
                    <ArrowUpRight size={17} strokeWidth={1.8} />
                </a>
            {/if}
        </div>

        <!-- Mobile Menu Button -->
        <button
            type="button"
            class="mobile-toggle"
            onclick={() => (menuOpen = !menuOpen)}
            aria-expanded={menuOpen}
            aria-label={menuOpen ? m.nav_menu_close() : m.nav_menu_open()}
        >
            {#if menuOpen}
                <X size={25} strokeWidth={1.7} />
            {:else}
                <Menu size={25} strokeWidth={1.7} />
            {/if}
        </button>
    </div>

    <!-- Mobile Navigation -->
    {#if menuOpen}
        <div class="mobile-navigation">

            <!-- Sprachwechsel Mobile -->
            <div class="mobile-language-row">
                <span>{m.nav_language_label()}</span>

                <div class="language-switch">
                    <button
                        type="button"
                        class:active={selectedLocale === 'de'}
                        aria-pressed={selectedLocale === 'de'}
                        onclick={() => changeLanguage('de')}
                    >
                        DE
                    </button>

                    <span class="language-separator">|</span>

                    <button
                        type="button"
                        class:active={selectedLocale === 'sq'}
                        aria-pressed={selectedLocale === 'sq'}
                        onclick={() => changeLanguage('sq')}
                    >
                        SQ
                    </button>

                    <span class="language-separator">|</span>

                    <button
                        type="button"
                        class:active={selectedLocale === 'en'}
                        aria-pressed={selectedLocale === 'en'}
                        onclick={() => changeLanguage('en')}
                    >
                        EN
                    </button>
                </div>
            </div>

            {#if $isLoggedIn}
                <div class="mobile-profile">
                    <span class="avatar">
                            {#if profileAvatar && failedAvatar !== profileAvatar}
                                <img
                                    src={profileAvatar}
                                    alt=""
                                    onerror={() => failedAvatar = profileAvatar}
                                />
                            {:else}
                                {profileInitial}
                            {/if}
                        </span>

                    <div class="mobile-profile-text">
                        <strong>{profileName}</strong>
                        <small>{$currentUser?.email || ''}</small>
                    </div>
                </div>
            {/if}

            <a
                href={resolve('/')}
                onclick={closeMenu}
                class="mobile-link"
            >
                <House size={19} />
                {m.nav_start()}
            </a>

            <a
                href={resolve('/jobs')}
                onclick={closeMenu}
                class="mobile-link"
            >
                <BriefcaseBusiness size={19} />
                {m.nav_jobs_services()}
            </a>

            <a
                href={resolve('/landing')}
                onclick={closeMenu}
                class="mobile-link"
            >
                <Info size={19} />
                {m.nav_how_nextjob_works()}
            </a>

            {#if $isLoggedIn}
                {#if accountType === 'jobnehmer'}
                    <a
                        href={resolve('/jobnehmer/profil')}
                        onclick={closeMenu}
                        class="mobile-link"
                    >
                        <UserRound size={19} />
                        {m.nav_my_profile()}
                    </a>
                {/if}

                <a
                    href={resolve('/chat')}
                    onclick={closeMenu}
                    class="mobile-link"
                >
                    <MessageCircle size={19} />
                    {m.nav_messages()}
                </a>

                <a
                    href={resolve('/benachrichtigungen')}
                    onclick={closeMenu}
                    class="mobile-link"
                >
                    <Bell size={19} />
                    {m.nav_notifications()}
                </a>

                <button
                    type="button"
                    onclick={handleLogout}
                    class="mobile-logout"
                >
                    <LogOut size={19} />
                    {m.nav_logout()}
                </button>
            {:else}
                <a
                    href={resolve('/auth/login')}
                    onclick={closeMenu}
                    class="mobile-link"
                >
                    <UserRound size={19} />
                    {m.nav_login()}
                </a>

                <a
                    href={resolve('/auth/register')}
                    onclick={closeMenu}
                    class="mobile-register"
                >
                    {m.nav_register()}
                    <ArrowUpRight size={19} />
                </a>
            {/if}
        </div>
    {/if}

    <!-- E-Mail Verification -->
    {#if emailUnverified}
        <div class="verification-notice">
            <span>{m.nav_verify_notice()}</span>

            <a href={resolve('/auth/verifizierung')}>
                {m.nav_verify_action()}
                <ArrowUpRight size={15} />
            </a>
        </div>
    {/if}
</nav>

<style>
    .nextjob-nav {
        position: sticky;
        top: 0;
        z-index: 50;
        background: var(--color-off-white);
        color: var(--color-charcoal);
        font-family: var(--font-body);
        border-bottom: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    }

    .nav-container {
        max-width: 1600px;
        margin: 0 auto;
        padding: 0 clamp(24px, 4.2vw, 88px);
        min-height: 82px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 16px;
    }

    .brand {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        flex-shrink: 0;
        text-decoration: none;
        color: inherit;
    }

    .brand-logo {
        height: 42px;
        width: auto;
        object-fit: contain;
    }

    .brand-name {
        font-family: var(--font-display);
        font-size: 22px;
        font-weight: 700;
        letter-spacing: -0.035em;
    }

    /* Suche */
    .search-wrapper {
        position: relative;
        flex: 0 1 330px;
        min-width: 0;
    }

    .nav-search {
        display: flex;
        align-items: center;
        gap: 10px;
        width: 100%;
        min-height: 46px;
        padding: 0 7px 0 15px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 13%, transparent);
        border-radius: 7px;
        background: transparent;
        transition: border-color 0.2s, background 0.2s;
    }

    .nav-search:focus-within {
        border-color: var(--color-fresh);
        background: var(--color-off-white);
    }

    .nav-search :global(.search-icon) {
        flex-shrink: 0;
        color: var(--color-charcoal);
        opacity: 0.6;
    }

    .nav-search input {
        flex: 1;
        width: 100%;
        min-width: 0;
        padding: 11px 0;
        border: 0;
        outline: 0;
        background: transparent;
        color: var(--color-charcoal);
        font-family: var(--font-body);
        font-size: 13px;
    }

    .nav-search input::placeholder {
        color: var(--color-charcoal);
        opacity: 0.55;
    }

    .nav-search input::-webkit-search-cancel-button {
        display: none;
    }

    .search-clear,
    .search-submit {
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        border: 0;
        cursor: pointer;
    }

    .search-clear {
        width: 26px;
        height: 30px;
        background: transparent;
        color: var(--color-charcoal);
        opacity: 0.65;
    }

    .search-submit {
        width: 32px;
        height: 32px;
        border-radius: 5px;
        background: var(--color-charcoal);
        color: var(--color-off-white);
        transition: background 0.2s;
    }

    .search-submit:hover:not(:disabled) {
        background: var(--color-fresh);
        color: var(--color-charcoal);
    }

    .search-submit:disabled {
        opacity: 0.35;
        cursor: not-allowed;
    }

    .search-panel {
        position: absolute;
        top: calc(100% + 10px);
        left: 0;
        width: 100%;
        min-width: 290px;
        padding: 16px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
        border-radius: 8px;
        background: var(--color-off-white);
        box-shadow: 0 15px 35px
            color-mix(in srgb, var(--color-charcoal) 10%, transparent);
        z-index: 60;
    }

    .search-panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 15px;
    }

    .search-panel-header span {
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 0.13em;
        opacity: 0.65;
    }

    .search-panel-header button {
        display: flex;
        align-items: center;
        justify-content: center;
        border: 0;
        background: transparent;
        color: var(--color-charcoal);
        cursor: pointer;
    }

    .search-filters {
        display: flex;
        gap: 7px;
    }

    .search-filters button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        padding: 9px 11px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
        border-radius: 5px;
        background: transparent;
        color: var(--color-charcoal);
        font-family: var(--font-body);
        font-size: 12px;
        cursor: pointer;
        transition: background 0.2s;
    }

    .search-filters button:hover {
        background: var(--color-sage);
    }

    .search-filters button.chosen {
        border-color: var(--color-sage);
        background: var(--color-sage);
        font-weight: 600;
    }

    .search-help {
        margin: 14px 0 0;
        font-size: 11px;
        line-height: 1.5;
        opacity: 0.65;
    }

    /* Desktop Navigation */
    .desktop-navigation,
    .desktop-actions {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .desktop-navigation {
        margin-left: auto;
    }

    .public-link {
        display: inline-flex;
        align-items: center;
        padding: 12px 15px;
        font-size: 14px;
        font-weight: 500;
        color: var(--color-charcoal);
        text-decoration: none;
        transition: color 0.2s;
    }

    .public-link:hover,
    .public-link.active {
        color: var(--color-fresh);
    }

    .nav-icon-link {
        display: flex;
        min-width: 75px;
        align-items: center;
        justify-content: center;
        flex-direction: column;
        gap: 6px;
        padding: 13px 9px 10px;
        border-bottom: 2px solid transparent;
        color: var(--color-charcoal);
        font-size: 11px;
        font-weight: 500;
        text-decoration: none;
        transition: color 0.2s, border-color 0.2s;
    }

    .nav-icon-link:hover,
    .nav-icon-link.active {
        color: var(--color-fresh);
        border-bottom-color: var(--color-fresh);
    }

    .login-link {
        padding: 11px 12px;
        color: var(--color-charcoal);
        font-size: 14px;
        font-weight: 500;
        text-decoration: none;
    }

    .login-link:hover {
        color: var(--color-fresh);
    }

    .register-button {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        gap: 16px;
        min-height: 46px;
        padding: 12px 17px;
        background: var(--color-charcoal);
        color: var(--color-off-white);
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        transition: background 0.2s;
    }

    .register-button:hover {
        background: var(--color-fresh);
        color: var(--color-charcoal);
    }

    /* Sprachwechsel */
    .language-switch {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        margin-right: 8px;
        white-space: nowrap;
    }

    .language-switch button {
        border: 0;
        padding: 7px 3px;
        background: transparent;
        color: var(--color-charcoal);
        font-family: var(--font-body);
        font-size: 13px;
        font-weight: 600;
        opacity: 0.5;
        cursor: pointer;
        transition: opacity 0.2s, color 0.2s;
    }

    .language-switch button:hover {
        opacity: 1;
    }

    .language-switch button.active {
        opacity: 1;
        color: var(--color-fresh);
    }

    .language-separator {
        color: var(--color-charcoal);
        opacity: 0.3;
        font-size: 13px;
    }

    /* Profile */
    .profile-container {
        position: relative;
    }

    .profile-trigger {
        display: flex;
        align-items: center;
        gap: 7px;
        padding: 5px;
        border: 0;
        background: transparent;
        color: var(--color-charcoal);
        cursor: pointer;
    }

    .avatar {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 39px;
        height: 39px;
        flex-shrink: 0;
        background: var(--color-sage);
        color: var(--color-charcoal);
        font-family: var(--font-display);
        font-size: 17px;
        font-weight: 600;
    }

    .profile-dropdown {
        position: absolute;
        right: 0;
        top: calc(100% + 13px);
        width: 250px;
        padding: 8px;
        background: var(--color-off-white);
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 15%, transparent);
        box-shadow: 0 15px 35px
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
        z-index: 70;
    }

    .profile-info {
        padding: 12px;
        margin-bottom: 7px;
        border-bottom: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    }

    .profile-name {
        font-size: 14px;
        font-weight: 600;
        overflow-wrap: anywhere;
    }

    .profile-email {
        margin-top: 5px;
        font-size: 11px;
        opacity: 0.65;
        overflow-wrap: anywhere;
    }

    .dropdown-link {
        display: flex;
        align-items: center;
        gap: 11px;
        width: 100%;
        padding: 12px;
        border: 0;
        background: transparent;
        color: var(--color-charcoal);
        font-size: 13px;
        text-align: left;
        text-decoration: none;
        cursor: pointer;
    }

    .dropdown-link:hover {
        background: var(--color-sage);
    }

    .logout-link {
        font-weight: 600;
    }

    /* Mobile */
    .mobile-toggle {
        display: none;
        align-items: center;
        justify-content: center;
        width: 42px;
        height: 42px;
        border: 1px solid
            color-mix(in srgb, var(--color-charcoal) 20%, transparent);
        background: transparent;
        color: var(--color-charcoal);
        cursor: pointer;
    }

    .mobile-navigation {
        display: none;
        padding: 14px 24px 24px;
        background: var(--color-off-white);
        border-top: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    }

    .mobile-language-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        padding: 12px 10px;
        border-bottom: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
        font-size: 13px;
        font-weight: 500;
    }

    .mobile-language-row .language-switch {
        margin-right: 0;
    }

    .mobile-link {
        display: flex;
        align-items: center;
        gap: 13px;
        padding: 14px 10px;
        color: var(--color-charcoal);
        font-size: 14px;
        font-weight: 500;
        text-decoration: none;
    }

    .mobile-link:hover {
        background: var(--color-sage);
    }

    .mobile-profile {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 10px 18px;
        margin-bottom: 8px;
        border-bottom: 1px solid
            color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    }

    .mobile-profile-text {
        display: flex;
        flex-direction: column;
        min-width: 0;
        gap: 5px;
    }

    .mobile-profile-text strong {
        font-size: 14px;
    }

    .mobile-profile-text small {
        font-size: 11px;
        opacity: 0.65;
        overflow-wrap: anywhere;
    }

    .mobile-register,
    .mobile-logout {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 12px;
        width: 100%;
        margin-top: 12px;
        padding: 15px;
        border: 0;
        background: var(--color-charcoal);
        color: var(--color-off-white);
        font-size: 14px;
        font-weight: 600;
        text-decoration: none;
        cursor: pointer;
    }

    /* Verification */
    .verification-notice {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 10px;
        flex-wrap: wrap;
        padding: 12px 20px;
        background: var(--color-sage);
        font-size: 12px;
    }

    .verification-notice a {
        display: inline-flex;
        align-items: center;
        gap: 5px;
        color: var(--color-charcoal);
        font-weight: 600;
        text-decoration: underline;
        text-underline-offset: 3px;
    }

    /* Responsive */
    @media (max-width: 1350px) and (min-width: 951px) {
    .nav-container {
        flex-wrap: nowrap;
        gap: 12px;
    }

    .search-wrapper {
        order: 0;
        flex: 1 1 220px;
        min-width: 150px;
        max-width: 330px;
    }
}
    @media (max-width: 1150px) {
        .brand-name {
            font-size: 19px;
        }

        .desktop-navigation,
        .desktop-actions {
            gap: 4px;
        }

        .nav-icon-link {
            min-width: 65px;
            padding-inline: 6px;
        }
    }

    @media (max-width: 767px) {
        .desktop-navigation,
        .desktop-actions {
            display: none;
        }

        .mobile-toggle,
        .mobile-navigation {
            display: flex;
        }

        .mobile-navigation {
            flex-direction: column;
        }

        .nav-container {
            min-height: 72px;
            flex-wrap: wrap;
            padding-block: 12px;
        }

        .search-wrapper {
            order: 3;
            flex: 1 0 100%;
            max-width: none;
        }
    }

    @media (max-width: 420px) {
        .brand-logo {
            height: 36px;
        }

        .brand-name {
            font-size: 19px;
        }

        .nav-container {
            padding-inline: 20px;
        }

        .search-panel {
            min-width: 0;
        }
    }

    .nav-search {
        border-radius: 24px;
        min-height: 42px;
        padding-inline: 15px 6px;
    }

    .nav-search:hover {
        border-color: var(--color-sage);
    }

    .nav-search:focus-within {
        background: rgba(255, 255, 255, 0.35);
        box-shadow: 0 0 0 3px rgba(98, 170, 151, 0.08);
    }

    .search-submit {
        border-radius: 50%;
        background: rgba(168, 183, 158, 0.25);
        color: var(--color-charcoal);
    }

    .avatar {
        border-radius: 50%;
        overflow: hidden;
    }

    .avatar img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }

    .how-link {
        max-width: 115px;
        text-align: center;
        line-height: 1.25;
    }

    @media (max-width: 767px) {
        .desktop-navigation,
        .desktop-actions {
            display: none;
        }

        .mobile-toggle {
            display: flex;
        }

        .mobile-navigation {
            display: flex;
            flex-direction: column;
        }
    }

    @media (min-width: 951px) and (max-width: 1350px) {
        .nav-container {
            padding-inline: 24px;
            gap: 8px;
        }

        .nav-icon-link {
            min-width: 52px;
            padding-inline: 5px;
            font-size: 10px;
        }

        .desktop-navigation,
        .desktop-actions {
            gap: 5px;
        }

        .search-wrapper {
            min-width: 100px;
            flex: 1 1 180px;
        }

        .how-link {
            max-width: 90px;
        }
    }

    @media (min-width: 768px) {
        .desktop-navigation,
        .desktop-actions {
            display: flex;
            gap: 5px;
        }

        .mobile-toggle,
        .mobile-navigation {
            display: none;
        }

        .nav-container {
            flex-wrap: nowrap;
            padding-inline: 24px;
            gap: 10px;
        }

        .nav-icon-link {
            min-width: 48px;
            padding-inline: 5px;
            font-size: 10px;
        }

        .search-wrapper {
            flex: 1 1 180px;
            min-width: 90px;
        }

        .brand-name {
            font-size: 19px;
        }

        .how-link {
            max-width: 90px;
        }
    }
</style>