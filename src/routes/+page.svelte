
<script>
  import { onMount } from 'svelte';
  import { ArrowUpRight, ArrowRight, ArrowLeft, ArrowDown, MapPin, Plus, Hammer, Camera, BookOpen, Coffee, Download, Check } from '@lucide/svelte';
  import Reviews from '$lib/components/Reviews.svelte';
  import * as m from '$lib/paraglide/messages.js';

  let categoryViewport;
  let activeStep = $state(0);
  let ready = $state(false);
  let audience = $state('hire');
  let category = $state('');
  let location = $state('Shkodër');
  let description = $state('');
  let brief = $state('');

  const categories = $derived([
    { name: m.home_category_digital(), detail: m.home_category_digital_detail(), image: 'creative-work.jpg', alt: m.home_image_camera(), icon: Camera, position: 'center' },
    { name: m.home_category_tutoring(), detail: m.home_category_tutoring_detail(), image: 'tutoring.jpg', alt: m.home_image_tutoring(), icon: BookOpen, position: 'center' },
    { name: m.home_category_events(), detail: m.home_category_events_detail(), image: 'hospitality.jpg', alt: m.home_image_barista(), icon: Coffee, position: '74% center' },
    { name: m.home_category_home(), detail: m.home_category_home_detail(), image: 'carpenter-workshop.jpg', alt: m.home_image_carpenter(), icon: Hammer, position: '62% center' }
  ]);

  const steps = $derived([
    { title: m.home_step1_title(), text: m.home_step1_text(), image: 'creative-work.jpg', alt: m.home_image_camera() },
    { title: m.home_step2_title(), text: m.home_step2_text(), image: 'tutoring.jpg', alt: m.home_image_tutoring() },
    { title: m.home_step3_title(), text: m.home_step3_text(), image: 'carpenter-workshop.jpg', alt: m.home_image_carpenter_focus() }
  ]);

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
    brief = `${audience === 'hire' ? m.home_brief_project_heading() : m.home_brief_profile_heading()}\n\n${m.home_brief_service()}: ${category}\n${m.home_brief_location()}: ${location.trim()}\n\n${audience === 'hire' ? m.home_brief_need() : m.home_brief_offer()}:\n${description.trim()}\n\n${m.home_brief_next_steps()}:\n${audience === 'hire' ? m.home_brief_next_hire() : m.home_brief_next_work()}\n\n${m.home_brief_disclaimer()}`;
  }

  onMount(() => {
    ready = true;
  });
</script>

<svelte:head>
  <title>{m.home_meta_title()}</title>
  <meta name="description" content={m.home_meta_description()} />
  <noscript><style>.start-form-wrap form,.audience-switch{display:none!important}</style></noscript>
</svelte:head>

<div class="landing">
  <section class="hero page-pad" aria-labelledby="hero-title">
    <div class="hero-copy glass-sheet">
      <p class="eyebrow"><span class="status-dot"></span> {m.home_hero_eyebrow()}</p>
      <h1 id="hero-title"><span class="word-mask"><span class="hero-word">{m.home_hero_title1()}</span></span><span class="word-mask"><span class="hero-word">{m.home_hero_title2()}<span class="headline-dot">.</span></span></span></h1>
      <div class="hero-description">
        <p>{m.home_hero_description1()}<br />{m.home_hero_description2()}</p>
        <div class="hero-actions">
          <a class="button" href="#get-started" onclick={() => chooseAudience('hire')}>{m.home_find_professional()} <ArrowUpRight size={21} /></a>
          <a class="text-link" href="#get-started" onclick={() => chooseAudience('work')}>{m.home_find_work()} <ArrowRight size={18} /></a>
        </div>
      </div>
      <div class="hero-bottom"><p><MapPin size={16} /> {m.home_hero_location()} <strong>{m.home_location_name()}</strong></p><a href="#categories" aria-label={m.home_scroll_categories()}><ArrowDown size={22} /></a></div>
    </div>
    <figure class="hero-visual">
      <div class="hero-photo"><img src="/images/creative-work.jpg" alt={m.home_image_camera()} fetchpriority="high" width="1000" height="1500" /></div>
      <div class="photo-marker"><span class="marker-cross">+</span><span>{m.home_photo_marker1()}<br />{m.home_photo_marker2()}</span></div>
      <figcaption><span>{m.home_photo_caption()}</span><span>01 — NEXTJOB</span></figcaption>
    </figure>
  </section>

  <section class="intro-strip page-pad glass-sheet" aria-label={m.home_intro_aria()}>
    <div class="intro-label"><span class="section-number">{m.home_intro_number()}</span><ArrowUpRight size={45} strokeWidth={1.2} /></div>
    <h2>{m.home_intro_title1()}<br />{m.home_intro_title2()}</h2>
    <p>{m.home_intro_description()}</p>
  </section>

  <section id="categories" class="categories-section section-space" aria-labelledby="categories-title">
    <div class="section-heading page-pad">
      <div><p class="eyebrow">{m.home_categories_eyebrow()}</p><h2 id="categories-title">{m.home_categories_title1()}<br />{m.home_categories_title2()}</h2></div>
      <div class="section-aside"><p>{m.home_categories_aside1()}<br />{m.home_categories_aside2()}</p><span class="small-label">{m.home_explore_services()} <ArrowRight size={20} /></span></div>
    </div>
    <!-- svelte-ignore a11y_no_noninteractive_tabindex (Keyboard users can scroll this overflow region.) -->
    <div id="service-gallery" class="category-viewport" bind:this={categoryViewport} tabindex="0" role="region" aria-label={m.home_gallery_aria()}>
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
      <span>{m.home_gallery_note()}</span>
      <div class="gallery-controls">
        <span>{m.home_explore_services()}</span>
        <button type="button" aria-label={m.home_previous_services()} aria-controls="service-gallery" onclick={() => browseServices(-1)} disabled={!ready}><ArrowLeft size={19} /></button>
        <button type="button" aria-label={m.home_next_services()} aria-controls="service-gallery" onclick={() => browseServices(1)} disabled={!ready}><ArrowRight size={19} /></button>
      </div>
    </div>
  </section>

  <section id="how-it-works" class="how-section" aria-labelledby="how-title">
    <div class="how-layout page-pad">
      <div class="how-copy glass-dark">
        <p class="eyebrow">{m.home_how_eyebrow()}</p>
        <h2 id="how-title">{m.home_how_title1()}<br />{m.home_how_title2()}</h2>
        <p class="how-intro">{m.home_how_intro()}</p>
        <div class="steps" role="group" aria-label={m.home_steps_aria()}>
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
        <div class="how-caption"><span>{m.home_how_caption1()}<br />{m.home_how_caption2()}</span><Plus size={30} strokeWidth={1} /></div>
      </div>
    </div>
  </section>

  <Reviews />

  <section class="for-pros page-pad section-space" aria-labelledby="pros-title">
    <div class="pros-photo"><img src="/images/hospitality.jpg" alt={m.home_image_barista()} width="800" height="1200" loading="lazy" /><span class="image-tag">{m.home_pros_image_tag()}</span></div>
    <div class="pros-copy glass-sheet"><p class="eyebrow">{m.home_pros_eyebrow()}</p><h2 id="pros-title">{m.home_pros_title1()}<br />{m.home_pros_title2()}<br /><span class="outline-line">{m.home_pros_title3()}</span></h2><p>{m.home_pros_description()}</p><a class="button" href="#get-started" onclick={() => chooseAudience('work')}>{m.home_pros_action()} <ArrowUpRight size={20} /></a></div>
  </section>

  <section id="get-started" class="get-started page-pad section-space" aria-labelledby="start-title">
    <div class="start-copy"><p class="eyebrow">{m.home_start_eyebrow()}</p><h2 id="start-title">{m.home_start_title1()}<br />{m.home_start_title2()}<br />{m.home_start_title3()}<span>.</span></h2><p>{m.home_start_question()}</p><ArrowUpRight class="start-arrow" size={105} strokeWidth={1} /></div>
    <div class="start-form-wrap glass-sheet">
      <div class="audience-switch" aria-label={m.home_audience_aria()}><button class:chosen={audience === 'hire'} aria-pressed={audience === 'hire'} onclick={() => chooseAudience('hire')}>{m.home_audience_hire()}</button><button class:chosen={audience === 'work'} aria-pressed={audience === 'work'} onclick={() => chooseAudience('work')}>{m.home_audience_work()}</button></div>
      <h3>{audience === 'hire' ? m.home_form_heading_hire() : m.home_form_heading_work()}</h3>
      <noscript><p class="form-note">{m.home_noscript()}</p></noscript>
      <form onsubmit={createBrief}>
        <fieldset disabled={!ready}>
        <div class="form-row"><div class="field"><label for="category">{audience === 'hire' ? m.home_form_category_hire() : m.home_form_category_work()}</label><select id="category" bind:value={category} required><option value="" disabled>{m.home_form_select_category()}</option>{#each categories as service}<option>{service.name}</option>{/each}<option>{m.home_option_office()}</option><option>{m.home_option_other()}</option></select></div><div class="field"><label for="location">{m.home_form_location()}</label><input id="location" name="location" bind:value={location} required maxlength="100" placeholder={m.home_form_location_placeholder()} /></div></div>
        <div class="field"><label for="description">{audience === 'hire' ? m.home_form_description_hire() : m.home_form_description_work()}</label><textarea id="description" name="description" bind:value={description} required minlength="12" maxlength="2000" rows="3" placeholder={audience === 'hire' ? m.home_form_placeholder_hire() : m.home_form_placeholder_work()}></textarea></div>
        <button class="button submit-button" type="submit">{audience === 'hire' ? m.home_form_submit_hire() : m.home_form_submit_work()}<ArrowUpRight size={20} /></button>
        <p class="form-note">{m.home_form_note()}</p>
        </fieldset>
      </form>
      <div aria-live="polite">
        {#if brief}<div class="brief-result"><div><Check size={20} /><h4>{audience === 'hire' ? m.home_result_hire() : m.home_result_work()}</h4></div><p>{m.home_result_description()}</p><a class="text-link" href={'data:text/plain;charset=utf-8,' + encodeURIComponent(brief)} download={audience === 'hire' ? 'nextjob-projektbriefing.txt' : 'nextjob-vorstellung.txt'}>{m.home_download_brief()} <Download size={17} /></a></div>{/if}
      </div>
    </div>
  </section>

  <section class="faq-section page-pad section-space" aria-labelledby="faq-title"><div><p class="eyebrow">{m.home_faq_eyebrow()}</p><h2 id="faq-title">{m.home_faq_title()}</h2></div><div class="faq-list glass-sheet">
    <details><summary>{m.home_faq1_question()}<Plus size={21} /></summary><p>{m.home_faq1_answer()}</p></details>
    <details><summary>{m.home_faq2_question()}<Plus size={21} /></summary><p>{m.home_faq2_answer()}</p></details>
    <details><summary>{m.home_faq3_question()}<Plus size={21} /></summary><p>{m.home_faq3_answer()}</p></details>
    <details><summary>{m.home_faq4_question()}<Plus size={21} /></summary><p>{m.home_faq4_answer()}</p></details>
    <details><summary>{m.home_faq5_question()}<Plus size={21} /></summary><p>{m.home_faq5_answer()}</p></details>
  </div></section>
  <p class="photo-credit page-pad">{m.home_photo_credit()} · <a href="/photo-credits.txt" target="_blank" rel="noreferrer">{m.home_photo_credits_link()}</a></p>
</div>
