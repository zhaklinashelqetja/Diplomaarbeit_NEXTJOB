<script>
  import { page } from '$app/state';
</script>

<div class="flex min-h-[60vh] flex-col items-center justify-center px-4 text-center">
  <h1 class="text-6xl font-bold text-gray-900">{page.status}</h1>
  <p class="mt-4 text-lg text-gray-600">
    {page.error?.message ?? 'Diese Seite existiert nicht.'}
  </p>
  <a href="/" class="mt-6 rounded-lg bg-gray-900 px-5 py-2 text-white hover:bg-gray-700">
    Zurück zur Startseite
  </a>
</div>