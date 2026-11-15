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

  <section id="how-it-works" class="how-section" aria-labelledby="how-title">
    <div class="how-layout page-pad">
      <div class="how-copy glass-dark">
        <p class="eyebrow">02 / So funktioniert’s</p>
        <h2 id="how-title">Eine gute Verbindung.<br />Ein großartiger Start.</h2>
        <p class="how-intro">Dein nächstes Projekt in 3 einfachen Schritten.</p>
        <div class="steps" role="group" aria-label="Wähle einen Schritt, um sein Foto zu sehen">
          {#each steps as step, i}
            <button type="button" class="step-row" class:is-active={activeStep === i} aria-pressed={activeStep === i} aria-controls="step-photo" onclick={() => activeStep = i} disabled={!ready}>
              <span class="step-number">0{i + 1}</span><span><span class="step-title">{step.title}</span><span class="step-text">{step.text}</span></span><ArrowUpRight size={23} />
            </button>
          {/each}
        </div>
      </div>
      <div class="how-media">
        <div id="step-photo" class="step-images">
          <img class="step-image" data-step={activeStep} src={'/images/' + steps[activeStep].image} alt={steps[activeStep].alt} width="800" height="1000" loading="lazy" />
        </div>
        <div class="how-caption"><span>KLEINE ANFÄNGE.<br />SOLIDE ERGEBNISSE.</span><Plus size={30} strokeWidth={1} /></div>
      </div>
    </div>
  </section>

  <Reviews />

  <section class="for-pros page-pad section-space" aria-labelledby="pros-title">
    <div class="pros-photo"><img src="/images/hospitality.jpg" alt="Ein Barista bereitet Pour-over-Kaffee zu" width="800" height="1200" loading="lazy" /><span class="image-tag">DEIN KÖNNEN. DEIN NÄCHSTER SCHRITT.</span></div>
    <div class="pros-copy glass-sheet"><p class="eyebrow">03 / Für alle, die anpacken</p><h2 id="pros-title">Deine Fähigkeiten.<br />Deine nächste<br /><span class="outline-line">Chance.</span></h2><p>Du gestaltest, unterrichtest, organisierst, baust. NextJob entsteht, damit du deine Arbeit vorstellen und Menschen finden kannst, die sie brauchen.</p><a class="button" href="#get-started" onclick={() => chooseAudience('work')}>Finde deine nächste Chance <ArrowUpRight size={20} /></a></div>
  </section>

  <section id="get-started" class="get-started page-pad section-space" aria-labelledby="start-title">
    <div class="start-copy"><p class="eyebrow">04 / Dein nächster Schritt</p><h2 id="start-title">Jeder gute Job<br />beginnt mit<br />einem Gespräch<span>.</span></h2><p>Wie wird deins aussehen?</p><ArrowUpRight class="start-arrow" size={105} strokeWidth={1} /></div>
    <div class="start-form-wrap glass-sheet">
      <div class="audience-switch" aria-label="Wähle, was du brauchst"><button class:chosen={audience === 'hire'} aria-pressed={audience === 'hire'} onclick={() => chooseAudience('hire')}>Ich suche eine Fachperson</button><button class:chosen={audience === 'work'} aria-pressed={audience === 'work'} onclick={() => chooseAudience('work')}>Ich suche Arbeit</button></div>
      <h3>{audience === 'hire' ? 'Gib deinem Projekt einen Startpunkt.' : 'Sag deiner nächsten Kundschaft, was du machst.'}</h3>
      <noscript><p class="form-note">Aktiviere JavaScript, um ein Briefing zu erstellen und herunterzuladen. Alle Leistungen und Informationen auf dieser Seite kannst du trotzdem ansehen.</p></noscript>
      <form onsubmit={createBrief}>
        <fieldset disabled={!ready}>
        <div class="form-row"><div class="field"><label for="category">{audience === 'hire' ? 'Welche Art von Hilfe?' : 'Deine Leistung'}</label><select id="category" bind:value={category} required><option value="" disabled>Leistung auswählen</option>{#each categories as service}<option>{service.name}</option>{/each}<option>Büro- &amp; Verwaltungsunterstützung</option><option>Etwas anderes</option></select></div><div class="field"><label for="location">Wo?</label><input id="location" name="location" bind:value={location} required maxlength="100" placeholder="Stadt oder remote" /></div></div>
        <div class="field"><label for="description">{audience === 'hire' ? 'Ein paar Worte zum Job' : 'Ein paar Worte zu deinen Fähigkeiten'}</label><textarea id="description" name="description" bind:value={description} required minlength="12" maxlength="2000" rows="3" placeholder={audience === 'hire' ? 'Zum Beispiel: Ich brauche eine einfache Webseite für mein Café…' : 'Zum Beispiel: Ich unterrichte Englisch und helfe Schülern bei der Prüfungsvorbereitung…'}></textarea></div>
        <button class="button submit-button" type="submit">{audience === 'hire' ? 'Mein Projektbriefing erstellen' : 'Meine Vorstellung erstellen'}<ArrowUpRight size={20} /></button>
        <p class="form-note">Probier die Vorschau aus: Erstelle ein Briefing zum Herunterladen. Nichts wird veröffentlicht oder gesendet, und deine Angaben bleiben auf dieser Seite.</p>
        </fieldset>
      </form>
      <div aria-live="polite">
        {#if brief}<div class="brief-result"><div><Check size={20} /><h4>{audience === 'hire' ? 'Dein Projektbriefing ist fertig.' : 'Deine Vorstellung ist fertig.'}</h4></div><p>Behalte es, bearbeite es und nutze es, um dein nächstes Gespräch zu beginnen.</p><a class="text-link" href={'data:text/plain;charset=utf-8,' + encodeURIComponent(brief)} download={audience === 'hire' ? 'nextjob-projektbriefing.txt' : 'nextjob-vorstellung.txt'}>Briefing herunterladen <Download size={17} /></a></div>{/if}
      </div>
    </div>
  </section>

  <section class="faq-section page-pad section-space" aria-labelledby="faq-title"><div><p class="eyebrow">Ein bisschen mehr Klarheit</p><h2 id="faq-title">Gute Fragen.</h2></div><div class="faq-list glass-sheet">
    <details><summary>Für wen ist NextJob?<Plus size={21} /></summary><p>Für Menschen und Unternehmen, die Hilfe suchen, und für Fachleute, die ihr nächstes Projekt suchen. Das können Designer, Nachhilfelehrer, Fotografen, Eventhelfer oder Menschen sein, die zu Hause etwas reparieren können.</p></details>
    <details><summary>Wo geht es los?<Plus size={21} /></summary><p>In Shkodër, Albanien. Wir starten mit den Fähigkeiten und alltäglichen Projekten ganz in der Nähe.</p></details>
    <details><summary>Muss die Arbeit vor Ort stattfinden?<Plus size={21} /></summary><p>Das hängt vom Job ab. Eine Reparatur braucht jemanden vor Ort; Design, Texten und manche Nachhilfestunden können remote stattfinden. Besprecht direkt, wo und wie die Arbeit erledigt wird.</p></details>
    <details><summary>Kann ich jetzt gleich jemanden buchen?<Plus size={21} /></summary><p>Dies ist eine Vorschau der NextJob-Homepage. Du kannst Leistungen entdecken und ein Projektbriefing oder eine berufliche Vorstellung herunterladen. Live-Profile, Jobausschreibungen und Buchungen sind noch nicht angebunden.</p></details>
    <details><summary>Wer vereinbart Preis und Zeitplan?<Plus size={21} /></summary><p>Kunde und Fachperson sollten vor Arbeitsbeginn direkt vereinbaren, was der Job umfasst, was er kostet und wann er stattfindet.</p></details>
  </div></section>
  <p class="photo-credit page-pad">Illustrative Stock-Fotografie · <a href="/photo-credits.txt" target="_blank" rel="noreferrer">Bildnachweise</a></p>
</div>
