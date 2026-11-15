<script>
  import { onMount } from 'svelte';
  import { ArrowUpRight, ArrowRight, ArrowLeft, ArrowDown, MapPin, Plus, Hammer, Camera, BookOpen, Coffee, Download, Check } from '@lucide/svelte';
  import Reviews from '$lib/components/Reviews.svelte';

  let categoryViewport;
  let activeStep = $state(0);
  let ready = $state(false);
  let audience = $state('hire');
  let category = $state('');
  let location = $state('Shkodër');
  let description = $state('');
  let brief = $state('');

  const categories = [
    { name: 'Digital & Kreatives', detail: 'Webseiten, Design, Fotografie und Content.', image: 'creative-work.jpg', alt: 'Eine Frau arbeitet mit einer Kamera', icon: Camera, position: 'center' },
    { name: 'Nachhilfe & Sprachen', detail: 'Eine Prüfung steht an. Eine neue Sprache will gelernt sein.', image: 'tutoring.jpg', alt: 'Zwei Personen gehen gemeinsam Lernnotizen durch', icon: BookOpen, position: 'center' },
    { name: 'Events & Gastronomie', detail: 'Eine helfende Hand für einen vollen Samstag.', image: 'hospitality.jpg', alt: 'Ein Barista bereitet Pour-over-Kaffee zu', icon: Coffee, position: '74% center' },
    { name: 'Haus & praktische Hilfe', detail: 'Reparaturen, Verbesserungen und Jobs im Alltag.', image: 'carpenter-workshop.jpg', alt: 'Tischler misst Holz an einer Werkbank in der Werkstatt', icon: Hammer, position: '62% center' }
  ];
  const steps = [
    { title: 'Beschreibe den Job.', text: 'Eine Webseite, eine wöchentliche Nachhilfestunde oder eine Reparatur zu Hause. Sag, was du brauchst und wann du es brauchst.', image: 'creative-work.jpg', alt: 'Eine Frau arbeitet mit einer Kamera' },
    { title: 'Besprecht die Details.', text: 'Frag nach der Erfahrung, erkläre deine Prioritäten und entscheide, ob es gut passt.', image: 'tutoring.jpg', alt: 'Zwei Personen gehen gemeinsam Lernnotizen durch' },
    { title: 'Einigt euch und legt los.', text: 'Legt gemeinsam Umfang, Preis, Zeitplan und Ort fest. Stellt sicher, dass beide wissen, wie es weitergeht.', image: 'carpenter-workshop.jpg', alt: 'Tischler konzentriert sich auf ein Holzprojekt' }
  ];

  function chooseAudience(value) {
    audience = value;
    brief = '';
  }
  function chooseCategory(name) {
    chooseAudience('hire');
    category = name;
  }
  function browseServices(direction) {
    categoryViewport?.scrollBy({ left: direction * categoryViewport.clientWidth * 0.75, behavior: 'auto' });
  }
  function createBrief(event) {
    event.preventDefault();
    brief = `${audience === 'hire' ? 'MEIN NEXTJOB-PROJEKTBRIEFING' : 'MEINE NEXTJOB-BERUFLICHE VORSTELLUNG'}\n\nLeistung: ${category}\nOrt: ${location.trim()}\n\n${audience === 'hire' ? 'Was ich brauche' : 'Was ich anbiete'}:\n${description.trim()}\n\nNächste Schritte:\n${audience === 'hire' ? 'Besprich Umfang, Budget, Zeitplan und Ort mit einer Fachperson.' : 'Füge Arbeitsbeispiele hinzu und teile diese Vorstellung mit potenziellen Kundinnen und Kunden.'}\n\nErstellt mit der NextJob-Homepage-Vorschau. Dieses Briefing wurde weder veröffentlicht noch gesendet.`;
  }
  onMount(() => {
    ready = true;
  });
</script>

<svelte:head>
  <title>NextJob — Gute Arbeit beginnt hier.</title>
  <meta name="description" content="Eine lokale Verbindung für dein nächstes Projekt oder deine nächste Chance. Entdecke das NextJob-Homepage-Konzept für Shkodër." />
  <noscript><style>.start-form-wrap form,.audience-switch{display:none!important}</style></noscript>
</svelte:head>

<div class="landing">
  <section class="hero page-pad" aria-labelledby="hero-title">
    <div class="hero-copy glass-sheet">
      <p class="eyebrow"><span class="status-dot"></span> Lokale Fähigkeiten. Echte Chancen.</p>
      <h1 id="hero-title"><span class="word-mask"><span class="hero-word">Gute Arbeit.</span></span><span class="word-mask"><span class="hero-word">Genau hier<span class="headline-dot">.</span></span></span></h1>
      <div class="hero-description">
        <p>Eine Webseite für dein Geschäft. Hilfe vor der Prüfung.<br />Finde die richtige Person oder bring deine eigenen Fähigkeiten ein.</p>
        <div class="hero-actions">
          <a class="button" href="#get-started" onclick={() => chooseAudience('hire')}>Fachperson finden <ArrowUpRight size={21} /></a>
          <a class="text-link" href="#get-started" onclick={() => chooseAudience('work')}>Arbeit finden <ArrowRight size={18} /></a>
        </div>
      </div>
      <div class="hero-bottom"><p><MapPin size={16} /> Wir starten ganz in deiner Nähe. <strong>Shkodër, Albanien.</strong></p><a href="#categories" aria-label="Zu den Leistungen scrollen"><ArrowDown size={22} /></a></div>
    </div>
    <figure class="hero-visual">
      <div class="hero-photo"><img src="/images/creative-work.jpg" alt="Eine Frau arbeitet mit einer Kamera" fetchpriority="high" width="1000" height="1500" /></div>
      <div class="photo-marker"><span class="marker-cross">+</span><span>Ein Talent, das geteilt werden will.<br />Ein Job, der getan werden will.</span></div>
      <figcaption><span>DIE MENSCHEN HINTER DEN MÖGLICHKEITEN</span><span>01 — NEXTJOB</span></figcaption>
    </figure>
  </section>

  <section class="intro-strip page-pad glass-sheet" aria-label="Unser Zweck">
    <div class="intro-label"><span class="section-number">01 / DIE IDEE</span><ArrowUpRight size={45} strokeWidth={1.2} /></div>
    <h2>Verschiedene Fähigkeiten.<br />Dieselbe Stadt.</h2>
    <p>Dein Unternehmen braucht eine Webseite. Dein Kind braucht Hilfe in Mathe. Dein Café braucht am Samstag Unterstützung. Verschiedene Jobs, und irgendwo jemand, der weiß, wie es geht.</p>
  </section>

  <section id="categories" class="categories-section section-space" aria-labelledby="categories-title">
    <div class="section-heading page-pad">
      <div><p class="eyebrow">Finde die passende Hilfe</p><h2 id="categories-title">Dafür gibt es<br />das richtige Talent.</h2></div>
      <div class="section-aside"><p>Für dein Geschäft.<br />Für deinen Alltag.</p><span class="small-label">LEISTUNGEN ENTDECKEN <ArrowRight size={20} /></span></div>
    </div>
    <!-- svelte-ignore a11y_no_noninteractive_tabindex (Keyboard users can scroll this overflow region.) -->
    <div id="service-gallery" class="category-viewport" bind:this={categoryViewport} tabindex="0" role="region" aria-label="Leistungskategorien, horizontal scrollen zum Entdecken">
      <div class="category-track">
        {#each categories as service, i}
          <a class="category-item" href="#get-started" onclick={() => chooseCategory(service.name)}>
            <div class="category-photo"><img src={'/images/' + service.image} alt={service.alt} style:object-position={service.position} loading="lazy" width="800" height="1000" /><span class="category-index">0{i + 1}</span><span class="category-arrow"><ArrowUpRight size={25} /></span></div>
            <div class="category-caption"><h3>{service.name}</h3><service.icon size={24} strokeWidth={1.5} /></div>
            <p>{service.detail}</p>
          </a>
        {/each}
      </div>
    </div>
    <div class="gallery-note page-pad">
      <span>Verschiedene Fähigkeiten. Derselbe Stolz auf gute Arbeit.</span>
      <div class="gallery-controls">
        <span>LEISTUNGEN ENTDECKEN</span>
        <button type="button" aria-label="Vorherige Leistungen" aria-controls="service-gallery" onclick={() => browseServices(-1)} disabled={!ready}><ArrowLeft size={19} /></button>
        <button type="button" aria-label="Nächste Leistungen" aria-controls="service-gallery" onclick={() => browseServices(1)} disabled={!ready}><ArrowRight size={19} /></button>
      </div>
    </div>
  </section>
</div>
