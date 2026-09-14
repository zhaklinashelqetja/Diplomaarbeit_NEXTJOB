<script>
  let menuOpen = $state(false);
  import { locale, t } from '$lib/i18n.js';
</script>

<nav class="border-b border-gray-200 bg-white">
  <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-3">
    <a href="/" class="text-xl font-bold text-gray-900">NextJob</a>

    <!-- Desktop-Links -->
    <div class="hidden items-center gap-6 md:flex">
      <a href="/" class="text-gray-700 hover:text-gray-900">Start</a>
      <a href="/wer-wir-sind" class="text-gray-700 hover:text-gray-900">Wer wir sind</a>
      <a href="/auth/login" class="rounded-lg bg-gray-900 px-4 py-2 text-white hover:bg-gray-700">Login</a>
    </div>

    <!-- Mobile Burger-Button -->
    <button
      class="md:hidden"
      aria-label="Menü öffnen"
      onclick={() => (menuOpen = !menuOpen)}
    >
      ☰
    </button>

    <button onclick={() => locale.update((l) => (l === 'de' ? 'al' : 'de'))}>
  {$locale === 'de' ? 'AL' : 'DE'}
</button>
  </div>

  <!-- Mobile-Menü -->
  {#if menuOpen}
    <div class="flex flex-col gap-2 border-t border-gray-200 px-4 py-3 md:hidden">
      <a href="/" class="text-gray-700">Start</a>
      <a href="/wer-wir-sind" class="text-gray-700">Wer wir sind</a>
      <a href="/auth/login" class="text-gray-700">Login</a>
    </div>
  {/if}
</nav>