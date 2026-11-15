<script>
  import { Quote, Star } from '@lucide/svelte';

  const reviews = [
    {
      name: 'Elira K.',
      initials: 'EK',
      role: 'Sample customer',
      service: 'Digital & creative',
      quote: 'I needed a simple website for my shop. She helped me work out what to include, kept me updated, and showed me how to make changes myself.',
      tone: 'sage'
    },
    {
      name: 'Arben M.',
      initials: 'AM',
      role: 'Sample customer',
      service: 'Lessons & languages',
      quote: 'We went back over the parts of maths I had never quite understood. Being able to ask the same question twice made all the difference.',
      tone: 'blue'
    },
    {
      name: 'Sara D.',
      initials: 'SD',
      role: 'Sample professional',
      service: 'Events & hospitality',
      quote: 'The café needed someone for a busy weekend. We agreed on the hours and the pay beforehand, so I knew exactly what to expect on my first shift.',
      tone: 'fresh'
    }
  ];
</script>

<section id="reviews" class="reviews-section page-pad section-space" aria-labelledby="reviews-title">
  <div class="reviews-heading">
    <div>
      <p class="eyebrow">Reviews &amp; experiences</p>
      <h2 id="reviews-title">A little feedback.<br />A lot of confidence.</h2>
    </div>
    <div class="reviews-intro">
      <p>The communication. The care. The finished job.<br />The small things people remember.</p>
      <span class="preview-note">Design preview · Sample names and reviews</span>
    </div>
  </div>

  <div class="reviews-grid">
    {#each reviews as review}
      <figure class="review-card" class:sage={review.tone === 'sage'} class:blue={review.tone === 'blue'} class:fresh={review.tone === 'fresh'}>
        <div class="review-topline">
          <span class="service-label">{review.service}</span>
          <Quote size={22} strokeWidth={1.4} aria-hidden="true" />
        </div>
        <div class="review-stars" role="img" aria-label="Example rating: 5 out of 5 stars">
          {#each Array(5) as _}
            <Star size={16} strokeWidth={1.4} fill="currentColor" aria-hidden="true" />
          {/each}
        </div>
        <blockquote><p>“{review.quote}”</p></blockquote>
        <figcaption>
          <span class="review-avatar" aria-hidden="true">{review.initials}</span>
          <div class="review-person">
            <span class="review-name">{review.name}</span>
            <span class="review-role">{review.role}</span>
          </div>
          <span class="example-label">Example review</span>
        </figcaption>
      </figure>
    {/each}
  </div>
</section>

<style>
  .reviews-section {
    background: linear-gradient(135deg, color-mix(in srgb, var(--color-sage) 15%, var(--color-off-white)), var(--color-off-white) 55%, color-mix(in srgb, var(--color-soft-blue) 13%, var(--color-off-white)));
    border-top: 1px solid var(--line);
    border-bottom: 1px solid var(--line);
  }

  .reviews-heading {
    display: flex;
    align-items: flex-end;
    justify-content: space-between;
    gap: 36px;
    margin-bottom: 40px;
  }

  h2 {
    margin-top: 23px;
    font-size: clamp(42px, 4.6vw, 70px);
    line-height: 1.05;
    letter-spacing: -.055em;
  }

  .reviews-intro {
    max-width: 340px;
    padding-bottom: 5px;
  }

  .reviews-intro p {
    font-size: 14px;
    line-height: 1.7;
  }

  .preview-note {
    display: block;
    margin-top: 17px;
    font-size: 11px;
    line-height: 1.6;
    color: color-mix(in srgb, var(--color-charcoal) 79%, transparent);
  }

  .reviews-grid {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 20px;
  }

  .review-card {
    --review-tint: var(--color-sage);
    display: flex;
    flex-direction: column;
    min-width: 0;
    padding: clamp(24px, 2.3vw, 36px);
    border: 1px solid color-mix(in srgb, var(--color-charcoal) 12%, transparent);
    border-radius: 24px;
    background: linear-gradient(150deg, color-mix(in srgb, var(--color-off-white) 86%, transparent), color-mix(in srgb, var(--review-tint) 12%, transparent));
    box-shadow: inset 0 1px 0 var(--color-off-white), 0 8px 24px -16px color-mix(in srgb, var(--color-charcoal) 16%, transparent);
  }

  .review-card.blue { --review-tint: var(--color-soft-blue); }
  .review-card.fresh { --review-tint: var(--color-fresh); }

  .review-topline {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
  }

  .service-label {
    font-size: 10px;
    font-weight: 600;
    line-height: 1.5;
    letter-spacing: .6px;
    text-transform: uppercase;
  }

  .review-topline :global(svg) {
    flex-shrink: 0;
    color: color-mix(in srgb, var(--color-charcoal) 45%, var(--review-tint));
  }

  .review-stars {
    display: flex;
    gap: 4px;
    margin-top: 31px;
    color: color-mix(in srgb, var(--color-fresh) 60%, var(--color-charcoal));
  }

  blockquote {
    flex: 1;
    margin: 20px 0 32px;
    font-family: var(--font-quote);
    font-size: clamp(18px, 1.5vw, 23px);
    font-weight: 300;
    line-height: 1.55;
    letter-spacing: -.35px;
  }

  figcaption {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    column-gap: 12px;
    row-gap: 14px;
    padding-top: 22px;
    border-top: 1px solid color-mix(in srgb, var(--color-charcoal) 13%, transparent);
  }

  .review-avatar {
    display: grid;
    place-items: center;
    flex: 0 0 46px;
    width: 46px;
    height: 46px;
    border: 1px solid color-mix(in srgb, var(--color-charcoal) 8%, transparent);
    border-radius: 50%;
    background: color-mix(in srgb, var(--review-tint) 55%, var(--color-off-white));
    font-size: 13px;
    font-weight: 600;
    letter-spacing: .3px;
  }

  .review-person {
    display: flex;
    flex-direction: column;
    gap: 5px;
  }

  .review-name { font-size: 13px; font-weight: 600; }
  .review-role { font-size: 10px; }

  .example-label {
    margin-left: auto;
    font-size: 9px;
    line-height: 1.5;
    color: color-mix(in srgb, var(--color-charcoal) 74%, transparent);
  }

  @media (max-width: 1050px) {
    .reviews-heading { align-items: flex-start; }
    .reviews-intro { max-width: 280px; padding-top: 38px; }
    .review-card { padding: 24px; }
    .example-label { flex-basis: 100%; margin-left: 58px; }
  }

  @media (max-width: 760px) {
    .reviews-heading { display: block; margin-bottom: 30px; }
    .reviews-intro { max-width: none; padding-top: 23px; }
    .reviews-grid { grid-template-columns: 1fr; gap: 16px; }
    .review-card { padding: 26px; }
    .review-stars { margin-top: 25px; }
    blockquote { font-size: 21px; margin-bottom: 27px; }
    .example-label { flex-basis: auto; margin-left: auto; }
  }

  @media (max-width: 370px) {
    .review-card { padding: 22px; }
    .example-label { flex-basis: 100%; margin-left: 58px; }
  }
</style>
