<script>
  import { goto } from '$app/navigation';
  import { t } from '$lib/i18n.js';

  let email = $state('');
  let password = $state('');
  let error = $state('');

  async function login(e) {
    e.preventDefault();
    error = '';

    const res = await fetch('http://localhost:5000/api/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    });
    const data = await res.json();

    if (!res.ok) {
      error = data.error;
      return;
    }

    localStorage.setItem('token', data.token);
    goto('/');
  }
</script>

<div class="mx-auto max-w-md px-4 py-12">
  <h1 class="text-2xl font-bold">{$t('login_title')}</h1>

  <form onsubmit={login} class="mt-6 flex flex-col gap-4">
    <input type="email" bind:value={email} placeholder={$t('login_email')} class="border rounded-lg px-3 py-2" />
    <input type="password" bind:value={password} placeholder={$t('login_password')} class="border rounded-lg px-3 py-2" />

    {#if error}
      <p class="text-red-600 text-sm">{error}</p>
    {/if}

    <button type="submit" class="bg-gray-900 text-white rounded-lg px-4 py-2">{$t('login_button')}</button>
  </form>
</div>