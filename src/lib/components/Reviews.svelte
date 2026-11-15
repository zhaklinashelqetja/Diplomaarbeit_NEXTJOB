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

