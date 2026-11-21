
<script>
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { page } from '$app/state';
	import { isLoggedIn, currentUser, logout } from '$lib/auth.js';

	import {
		House,
		BriefcaseBusiness,
		MessageCircle,
		Bell,
		UserRound,
		Menu,
		X,
		ChevronDown,
		ArrowUpRight,
		LogOut,
		Search
	} from '@lucide/svelte';

	let menuOpen = $state(false);
	let profileOpen = $state(false);

	let accountType = $derived($currentUser?.account_type);

	let emailUnverified = $derived(
		$isLoggedIn &&
		$currentUser &&
		$currentUser.is_verified === false
	);

	let profileName = $derived(
		$currentUser?.name ||
		$currentUser?.username ||
		$currentUser?.email?.split('@')[0] ||
		'NextJob'
	);

	let profileInitial = $derived(
		profileName.charAt(0).toUpperCase()
	);

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
			aria-label="NextJob Startseite"
		>
			<img
				src="/images/nextjob-logo.png"
				alt="NextJob Logo"
				class="brand-logo"
			/>

			<span class="brand-name">NEXTJOB</span>
		</a>

		<!-- Desktop Navigation -->
		<div class="desktop-navigation">
			{#if $isLoggedIn}

				<a
					href={resolve('/')}
					class="nav-icon-link"
					class:active={isActive('/')}
					aria-current={isActive('/') ? 'page' : undefined}
				>
					<House size={21} strokeWidth={1.7} />
					<span>Start</span>
				</a>

				<a
					href={resolve('/jobs')}
					class="nav-icon-link"
					class:active={isActive('/jobs')}
					aria-current={isActive('/jobs') ? 'page' : undefined}
				>
					<BriefcaseBusiness size={21} strokeWidth={1.7} />
					<span>Jobs</span>
				</a>

				{#if accountType === 'jobnehmer'}
					<a
						href={resolve('/jobnehmer/hauptseite')}
						class="nav-icon-link"
						class:active={isActive('/jobnehmer/hauptseite')}
					>
						<UserRound size={21} strokeWidth={1.7} />
						<span>Mein Bereich</span>
					</a>
				{/if}

				<a
					href={resolve('/chat')}
					class="nav-icon-link"
					class:active={isActive('/chat')}
				>
					<MessageCircle size={21} strokeWidth={1.7} />
					<span>Nachrichten</span>
				</a>

				<a
					href={resolve('/benachrichtigungen')}
					class="nav-icon-link"
					class:active={isActive('/benachrichtigungen')}
				>
					<Bell size={21} strokeWidth={1.7} />
					<span>Mitteilungen</span>
				</a>

			{:else}

				<a
					href={resolve('/')}
					class="public-link"
					class:active={isActive('/')}
				>
					Start
				</a>

				<a
					href={resolve('/jobs')}
					class="public-link"
					class:active={isActive('/jobs')}
				>
					Jobs & Dienstleistungen
				</a>

			{/if}
		</div>

		<!-- Desktop Actions -->
		<div class="desktop-actions">
			{#if $isLoggedIn}

				<div class="profile-container">
					<button
						type="button"
						class="profile-trigger"
						onclick={() => (profileOpen = !profileOpen)}
						aria-expanded={profileOpen}
						aria-label="Profilmenü"
					>
						<span class="avatar">
							{profileInitial}
						</span>

						<ChevronDown
							size={15}
							strokeWidth={1.7}
						/>
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
									href={resolve('/jobnehmer/hauptseite')}
									onclick={closeMenu}
									class="dropdown-link"
								>
									<UserRound size={17} />
									Mein Bereich
								</a>
							{/if}

							<button
								type="button"
								class="dropdown-link logout-link"
								onclick={handleLogout}
							>
								<LogOut size={17} />
								Abmelden
							</button>
						</div>
					{/if}
				</div>

			{:else}

				<a
					href={resolve('/auth/login')}
					class="login-link"
				>
					Anmelden
				</a>

				<a
					href={resolve('/auth/register')}
					class="register-button"
				>
					Registrieren
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
			aria-label={menuOpen ? 'Menü schließen' : 'Menü öffnen'}
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

			{#if $isLoggedIn}
				<div class="mobile-profile">
					<span class="avatar">
						{profileInitial}
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
				Start
			</a>

			<a
				href={resolve('/jobs')}
				onclick={closeMenu}
				class="mobile-link"
			>
				<BriefcaseBusiness size={19} />
				Jobs & Dienstleistungen
			</a>

			{#if $isLoggedIn}

				{#if accountType === 'jobnehmer'}
					<a
						href={resolve('/jobnehmer/hauptseite')}
						onclick={closeMenu}
						class="mobile-link"
					>
						<UserRound size={19} />
						Mein Bereich
					</a>
				{/if}

				<a
					href={resolve('/chat')}
					onclick={closeMenu}
					class="mobile-link"
				>
					<MessageCircle size={19} />
					Nachrichten
				</a>

				<a
					href={resolve('/benachrichtigungen')}
					onclick={closeMenu}
					class="mobile-link"
				>
					<Bell size={19} />
					Benachrichtigungen
				</a>

				<button
					type="button"
					onclick={handleLogout}
					class="mobile-logout"
				>
					<LogOut size={19} />
					Abmelden
				</button>

			{:else}

				<a
					href={resolve('/auth/login')}
					onclick={closeMenu}
					class="mobile-link"
				>
					<UserRound size={19} />
					Anmelden
				</a>

				<a
					href={resolve('/auth/register')}
					onclick={closeMenu}
					class="mobile-register"
				>
					Registrieren
					<ArrowUpRight size={19} />
				</a>

			{/if}
		</div>
	{/if}

	<!-- E-Mail Verification -->
	{#if emailUnverified}
		<div class="verification-notice">
			<span>
				Bitte bestätige deine E-Mail-Adresse.
			</span>

			<a href={resolve('/auth/verifizierung')}>
				Jetzt bestätigen
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
		gap: 24px;
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

	@media (max-width: 1150px) {
		.nav-container {
			gap: 10px;
		}

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

	@media (max-width: 950px) {
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
	}
</style>
