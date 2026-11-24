
<script>
    import {
        ArrowUpRight, ArrowRight, Search, BriefcaseBusiness, Users,
        MessageCircle, Star, ShieldCheck, MapPin, ChevronDown,
        Wrench, Zap, Paintbrush, Construction, Trees, Sparkles,
        Monitor, Hammer, House
    } from '@lucide/svelte';

    let { data } = $props();
    let categories = $derived(data.categories);

    const categoryIcons = [
        Wrench, Zap, Paintbrush, Construction, Hammer,
        Trees, Sparkles, Paintbrush, Monitor
    ];

    const categoryImages = [
        'https://images.unsplash.com/photo-1607472586893-edb57bdc0e39?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1562259949-e8e7689d7828?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1601058268499-e5266a7c8b47?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1416879595882-3373a0480b5b?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1581578731548-c64695cc6952?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1541961017774-22349e4a1262?auto=format&fit=crop&w=900&q=80',
        'https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=900&q=80'
    ];

    let openFaq = $state(null);

    const faqs = [
        {
            question: 'Was ist NEXTJOB?',
            answer: 'NEXTJOB ist eine digitale Plattform, die Jobgeber und Jobnehmer miteinander verbindet. Jobgeber können Aufgaben und Projekte veröffentlichen, während Jobnehmer passende Jobs suchen und Angebote senden können.'
        },
        {
            question: 'Wie kann ich einen Job auf NEXTJOB veröffentlichen?',
            answer: 'Nach der Registrierung kannst du einen Job erstellen. Dabei gibst du einen Titel, eine Beschreibung, eine Kategorie, den Standort und weitere wichtige Informationen an. Anschließend kannst du den Job veröffentlichen.'
        },
        {
            question: 'Wie finde ich passende Jobs?',
            answer: 'Jobnehmer können die Jobsuche verwenden, um verfügbare Jobs zu durchsuchen. Mithilfe von Suchbegriffen und Filtern können sie passende Tätigkeiten entdecken und die Details der einzelnen Jobs ansehen.'
        },
        {
            question: 'Welche Dienstleistungen kann ich anbieten?',
            answer: 'Auf NEXTJOB können unterschiedliche Dienstleistungen angeboten werden, beispielsweise Bauarbeiten, Reinigung, Gartenpflege, Reparaturen, Grafikdesign, Marketing und digitale Dienstleistungen.'
        },
        {
            question: 'Wie kann ich ein Angebot senden?',
            answer: 'Wenn du einen passenden Job gefunden hast, kannst du die Jobdetails ansehen und ein Angebot für die gewünschte Arbeit senden. Der Jobgeber kann die Angebote anschließend vergleichen.'
        },
        {
            question: 'Kann ich mein Profil bearbeiten?',
            answer: 'Ja. Nutzer können ihre Profile verwalten und relevante Informationen, persönliche Angaben, Fähigkeiten und Erfahrungen ergänzen, damit andere Nutzer mehr über sie erfahren.'
        },
        {
            question: 'Kann ich NEXTJOB auf meinem Handy verwenden?',
            answer: 'NEXTJOB ist für verschiedene Bildschirmgrößen ausgelegt. Die Plattform kann auf Desktop-Computern, Tablets und Smartphones verwendet werden.'
        }
    ];
</script>

<svelte:head>
    <title>{data.seo.title}</title>
    <meta name="description" content={data.seo.description} />
    <meta name="keywords" content={data.seo.keywords} />
    <meta name="robots" content="index, follow" />
    <meta property="og:title" content={data.seo.title} />
    <meta property="og:description" content={data.seo.description} />
    <meta property="og:type" content="website" />
</svelte:head>

<div class="overflow-hidden bg-[#F5F1EE] text-[#2A2E38]">

    <!-- HERO -->
    <section class="grid items-center gap-14 px-6 py-20 md:px-[6%] lg:grid-cols-2 lg:gap-[5%] lg:py-24">
        <div>
            <div class="flex items-center gap-2.5 text-[11px] font-bold tracking-[2px] text-[#66766A]">
                <span class="h-2 w-2 bg-[#62AA97]"></span>
                DIE PLATTFORM FÜR LOKALE DIENSTLEISTUNGEN
            </div>

            <h1 class="my-7 text-5xl font-extrabold leading-[0.99] tracking-[-3px] md:text-7xl lg:text-[85px] lg:tracking-[-5px]">
                Gute Arbeit.
                <span class="block text-[#62AA97]">Die richtigen</span>
                Menschen.
            </h1>

            <p class="max-w-[550px] text-base leading-8 text-[#656871]">
                Finde passende Fachkräfte für deine Projekte oder entdecke
                neue Möglichkeiten, deine Fähigkeiten anzubieten.
                NEXTJOB verbindet Menschen und Dienstleistungen an einem Ort.
            </p>

            <div class="mt-8 flex flex-wrap gap-3.5">
                <a href="/jobs" class="inline-flex items-center justify-center gap-3 bg-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#62AA97]">
                    Jobs entdecken <ArrowUpRight size={18}/>
                </a>

                <a href="/register" class="inline-flex items-center justify-center gap-3 border border-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-[#2A2E38] transition hover:bg-[#2A2E38] hover:text-white">
                    Job veröffentlichen <ArrowRight size={18}/>
                </a>
            </div>

            <div class="mt-8 flex items-center gap-2.5 text-xs text-[#85868B]">
                <MapPin size={16}/>
                Lokale Dienstleistungen. Digitale Vermittlung.
            </div>
        </div>

        <div class="relative mt-6 min-h-[400px] lg:mt-0 lg:min-h-[500px]">
            <div class="h-[400px] bg-cover bg-center lg:h-[500px]"
                style="background-image: url('https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=85')">
            </div>

            <div class="absolute left-[-10px] top-8 flex max-w-[290px] items-center gap-3.5 bg-white p-4 shadow-xl md:left-[-40px]">
                <div class="flex h-11 w-11 shrink-0 items-center justify-center bg-[#E3EBE1] text-[#527362]">
                    <BriefcaseBusiness size={20}/>
                </div>
                <div>
                    <strong class="text-[13px]">Neue Möglichkeiten</strong>
                    <p class="mt-1 text-[11px] text-[#85868B]">Jobs entdecken und Angebote senden</p>
                </div>
            </div>

            <div class="absolute bottom-8 right-[-10px] flex max-w-[290px] items-center gap-3.5 bg-white p-4 shadow-xl md:right-[-25px]">
                <div class="flex h-11 w-11 shrink-0 items-center justify-center bg-[#E1EAF0] text-[#587A91]">
                    <Users size={20}/>
                </div>
                <div>
                    <strong class="text-[13px]">Menschen verbinden</strong>
                    <p class="mt-1 text-[11px] text-[#85868B]">Jobgeber & Jobnehmer</p>
                </div>
            </div>

            <div class="absolute -bottom-9 left-0 text-[10px] tracking-[2px] text-[#777982]">
                <span class="text-[#62AA97]">01 /</span> LOKALE DIENSTLEISTUNGEN
            </div>
        </div>
    </section>

    <!-- INTRO -->
    <section class="bg-[#E9E6E1] px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">01 — ÜBER NEXTJOB</div>

        <div class="mt-10 grid gap-10 lg:grid-cols-2 lg:gap-[10%]">
            <h2 class="text-4xl leading-tight tracking-[-2px] md:text-5xl">
                Dienstleistungen finden.
                <span class="block text-[#62AA97]">Arbeit vermitteln.</span>
                Einfach verbinden.
            </h2>

            <div>
                <p class="mb-5 text-[15px] leading-8 text-[#656871]">
                    Die Suche nach geeigneten Personen für bestimmte Aufgaben
                    kann zeitaufwendig sein. NEXTJOB bietet eine digitale
                    Möglichkeit, Jobs zu veröffentlichen, Dienstleistungen
                    anzubieten und passende Angebote zu finden.
                </p>

                <p class="mb-5 text-[15px] leading-8 text-[#656871]">
                    Von handwerklichen Arbeiten und Reparaturen bis hin zu
                    kreativen und digitalen Projekten – NEXTJOB bringt
                    verschiedene Dienstleistungen auf einer Plattform zusammen.
                </p>

                <a href="#how-it-works" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                    Die Plattform kennenlernen <ArrowRight size={18}/>
                </a>
            </div>
        </div>
    </section>

    <!-- HOW IT WORKS -->
    <section id="how-it-works" class="px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">02 — DER ABLAUF</div>

        <div class="mb-12 mt-9">
            <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">Wie funktioniert NEXTJOB?</h2>
            <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                Vier Schritte, um Jobgeber und Jobnehmer miteinander zu verbinden.
            </p>
        </div>

        <div class="grid grid-cols-1 border-y border-[#2A2E38]/20 md:grid-cols-2 lg:grid-cols-4">
            {#each [
                {number:'01',icon:Users,title:'Account erstellen',text:'Registriere dich auf NEXTJOB und erstelle dein persönliches Profil, um die Plattform zu verwenden.'},
                {number:'02',icon:Search,title:'Jobs entdecken',text:'Suche nach verfügbaren Jobs, entdecke unterschiedliche Kategorien und finde Aufgaben, die zu deinen Fähigkeiten passen.'},
                {number:'03',icon:BriefcaseBusiness,title:'Jobs veröffentlichen',text:'Jobgeber können ihre Aufgaben beschreiben, wichtige Details hinzufügen und Jobs für andere Nutzer sichtbar machen.'},
                {number:'04',icon:MessageCircle,title:'Kontakt aufnehmen',text:'Angebote senden, Informationen austauschen und die Zusammenarbeit rund um einen Job organisieren.'}
            ] as step,i}
                <article class="border-b border-[#2A2E38]/15 p-7 md:border-r md:nth-[2]:border-r-0 lg:border-b-0 lg:border-r lg:nth-[2]:border-r lg:last:border-r-0">
                    <div class="text-xs font-bold text-[#62AA97]">{step.number}</div>
                    <div class="my-8 text-[#527362]">
                        <step.icon size={25}/>
                    </div>
                    <h3 class="mb-4 text-xl font-semibold">{step.title}</h3>
                    <p class="text-[13px] leading-7 text-[#777982]">{step.text}</p>
                </article>
            {/each}
        </div>
    </section>

    <!-- CATEGORIES -->
    <section id="categories" class="bg-[#E9E6E1] px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">03 — DIENSTLEISTUNGEN</div>

        <div class="mb-12 mt-9 flex flex-col items-start justify-between gap-6 lg:flex-row lg:items-end">
            <div>
                <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">Welche Arbeiten findest du auf NEXTJOB?</h2>
                <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                    Entdecke unterschiedliche Dienstleistungen, Projekte und Aufgaben in verschiedenen Arbeitsbereichen.
                </p>
            </div>

            <a href="/jobs" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                Jobs durchsuchen <ArrowRight size={18}/>
            </a>
        </div>

        <div class="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {#each categories as category,i}
                <article class="border border-[#2A2E38]/10 bg-[#F5F1EE] transition duration-300 hover:-translate-y-1">
                    <div class="relative h-[230px] bg-cover bg-center" style={`background-image: url('${categoryImages[i % categoryImages.length]}')`}>
                        <div class="absolute inset-0 bg-gradient-to-t from-[#2A2E38]/50 to-transparent"></div>

                        <div class="absolute bottom-5 left-5 flex h-12 w-12 items-center justify-center bg-[#F5F1EE] text-[#2A2E38]">
                            {#if categoryIcons[i]}
                                <svelte:component this={categoryIcons[i]} size={23}/>
                            {/if}
                        </div>

                        <span class="absolute right-5 top-5 text-[11px] tracking-wide text-white">
                            0{i + 1}
                        </span>
                    </div>

                    <div class="p-6">
                        <h3 class="mb-3 text-xl font-semibold">{category.name}</h3>

                        <p class="text-[13px] leading-7 text-[#777982]">
                            {category.description}
                        </p>

                        <div class="my-5 flex flex-wrap gap-2">
                            {#each category.examples as example}
                                <span class="bg-[#E9E6E1] px-2.5 py-2 text-[10px] text-[#656871]">
                                    {example}
                                </span>
                            {/each}
                        </div>

                        <a href="/jobs" class="flex items-center justify-between border-t border-[#2A2E38]/10 pt-4 text-xs font-bold transition hover:text-[#62AA97]">
                            Jobs entdecken <ArrowUpRight size={17}/>
                        </a>
                    </div>
                </article>
            {/each}
        </div>
    </section>

    <!-- JOBGEBER -->
    <section id="jobgeber" class="grid gap-12 bg-[#2A2E38] px-6 py-20 text-[#F5F1EE] md:px-[6%] lg:grid-cols-2 lg:gap-[8%] lg:py-24">
        <div class="relative min-h-[400px] bg-cover bg-center lg:min-h-[680px]"
            style="background-image: url('https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=1200&q=85')">
            <div class="absolute bottom-6 left-6 right-6 bg-[#2A2E38]/90 p-6 text-white">
                <span class="text-[11px] tracking-[2px] text-[#A8B79E]">FÜR JOBGEBER</span>
                <p class="mb-0 text-xl">Die passende Unterstützung für dein Projekt.</p>
            </div>
        </div>

        <div>
            <div class="text-[11px] font-bold tracking-[2px] text-[#A8B79E]">04 — JOBGEBER</div>

            <h2 class="my-8 text-4xl font-bold leading-tight tracking-[-2px] md:text-5xl">
                Deine Aufgabe.
                <span class="block text-[#62AA97]">Dein Auftrag.</span>
            </h2>

            <p class="mb-9 text-sm leading-8 text-[#C0C2C8]">
                Du benötigst Unterstützung für eine bestimmte Arbeit?
                Mit NEXTJOB kannst du deinen Job beschreiben und
                Informationen bereitstellen, damit Jobnehmer deine
                Aufgabe besser verstehen.
            </p>

            <div class="mb-9">
                {#each [
                    {title:'Registrieren und anmelden',text:'Erstelle ein Konto, um Jobs veröffentlichen zu können.'},
                    {title:'Jobbeschreibung erstellen',text:'Gib einen Titel, die Kategorie, den Standort, das Budget und eine ausführliche Beschreibung an.'},
                    {title:'Job veröffentlichen',text:'Veröffentliche deine Aufgabe, damit interessierte Jobnehmer sie entdecken können.'},
                    {title:'Angebote vergleichen',text:'Prüfe die eingegangenen Angebote und Profile der Jobnehmer.'},
                    {title:'Zusammenarbeit planen',text:'Kläre weitere Details mit einem passenden Jobnehmer.'}
                ] as instruction,i}
                    <div class="flex gap-5 border-b border-white/10 py-5">
                        <span class="pt-1 text-xs font-bold text-[#62AA97]">0{i+1}</span>
                        <div>
                            <h3 class="mb-2 text-[15px] font-semibold">{instruction.title}</h3>
                            <p class="m-0 text-xs leading-7 text-[#C0C2C8]">{instruction.text}</p>
                        </div>
                    </div>
                {/each}
            </div>

            <a href="/register" class="inline-flex items-center gap-3 bg-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#62AA97]">
                Jetzt Job veröffentlichen <ArrowUpRight size={18}/>
            </a>
        </div>
    </section>

    <!-- JOBNEHMER -->
    <section id="jobnehmer" class="grid gap-12 px-6 py-20 md:px-[6%] lg:grid-cols-2 lg:gap-[8%] lg:py-24">
        <div>
            <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">05 — JOBNEHMER</div>

            <h2 class="my-8 text-4xl font-bold leading-tight tracking-[-2px] md:text-5xl">
                Deine Fähigkeiten.
                <span class="block text-[#62AA97]">Neue Möglichkeiten.</span>
            </h2>

            <p class="mb-9 text-sm leading-8 text-[#777982]">
                Du bietest Dienstleistungen an und suchst neue Aufgaben?
                Auf NEXTJOB kannst du dein Profil präsentieren, verfügbare
                Jobs entdecken und passende Angebote senden.
            </p>

            <div class="mb-9">
                {#each [
                    {title:'Profil erstellen',text:'Ergänze persönliche Informationen und beschreibe deine Dienstleistungen.'},
                    {title:'Erfahrung zeigen',text:'Stelle deine Fähigkeiten, Erfahrungen und Arbeitsbereiche vor.'},
                    {title:'Passende Jobs suchen',text:'Durchsuche Jobs und nutze die verfügbaren Suchfunktionen.'},
                    {title:'Interessante Jobs speichern',text:'Speichere Jobs, die du später erneut ansehen möchtest.'},
                    {title:'Angebote senden',text:'Sende dem Jobgeber ein Angebot für die gewünschte Arbeit.'}
                ] as instruction,i}
                    <div class="flex gap-5 border-b border-[#2A2E38]/10 py-5">
                        <span class="pt-1 text-xs font-bold text-[#62AA97]">0{i+1}</span>
                        <div>
                            <h3 class="mb-2 text-[15px] font-semibold">{instruction.title}</h3>
                            <p class="m-0 text-xs leading-7 text-[#777982]">{instruction.text}</p>
                        </div>
                    </div>
                {/each}
            </div>

            <a href="/jobs" class="inline-flex items-center gap-3 bg-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#62AA97]">
                Jobs entdecken <ArrowUpRight size={18}/>
            </a>
        </div>

        <div class="relative min-h-[400px] bg-cover bg-center lg:min-h-[680px]"
            style="background-image: url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=85')">
            <div class="absolute bottom-6 left-6 right-6 bg-[#2A2E38]/85 p-6 text-white">
                <span class="text-[11px] tracking-[2px] text-[#A8B79E]">FÜR JOBNEHMER</span>
                <p class="mb-0 text-xl">Fähigkeiten zeigen. Chancen entdecken.</p>
            </div>
        </div>
    </section>

    <!-- FEATURES -->
    <section class="bg-[#E9E6E1] px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">06 — DIE PLATTFORM</div>

        <div class="mb-12 mt-9">
            <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">Mehr als nur eine Jobsuche.</h2>
            <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                Funktionen, die die Vermittlung und Organisation von Dienstleistungen erleichtern.
            </p>
        </div>

        <div class="grid grid-cols-1 border-l border-t border-[#2A2E38]/20 md:grid-cols-2 xl:grid-cols-3">
            {#each [
                {icon:Search,title:'Gezielte Jobsuche',text:'Suche nach verfügbaren Aufgaben und entdecke unterschiedliche Dienstleistungen.'},
                {icon:Users,title:'Persönliche Profile',text:'Nutzer können Informationen, Erfahrungen und Fähigkeiten auf ihren Profilen präsentieren.'},
                {icon:MessageCircle,title:'Kommunikation',text:'Die Plattform ermöglicht den Austausch zwischen Jobgebern und Jobnehmern.'},
                {icon:Star,title:'Bewertungen',text:'Bewertungen können dabei helfen, Erfahrungen mit anderen Nutzern einzuschätzen.'},
                {icon:ShieldCheck,title:'Übersichtliche Verwaltung',text:'Nutzer können ihre Jobs, Profile und Aktivitäten auf der Plattform verwalten.'},
                {icon:House,title:'Mobile Nutzung',text:'NEXTJOB ist auf unterschiedlichen Geräten zugänglich und für mobile Ansichten ausgelegt.'}
            ] as feature}
                <article class="border-b border-r border-[#2A2E38]/20 p-8">
                    <feature.icon size={24} class="text-[#527362]"/>
                    <h3 class="mt-6 text-lg font-semibold">{feature.title}</h3>
                    <p class="text-[13px] leading-7 text-[#777982]">{feature.text}</p>
                </article>
            {/each}
        </div>
    </section>

    <!-- FAQ -->
    <section id="faq" class="px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">07 — FRAGEN & ANTWORTEN</div>

        <div class="mt-9 grid gap-10 lg:grid-cols-[0.7fr_1.3fr] lg:gap-[10%]">
            <div>
                <h2 class="text-4xl font-bold leading-tight tracking-[-2px]">Häufig gestellte Fragen.</h2>
                <p class="my-6 text-sm leading-8 text-[#777982]">
                    Antworten auf die wichtigsten Fragen rund um NEXTJOB und die Verwendung der Plattform.
                </p>

                <a href="/register" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                    NEXTJOB ausprobieren <ArrowRight size={18}/>
                </a>
            </div>

            <div>
                {#each faqs as faq,i}
                    <article class="border-b border-[#2A2E38]/15">
                        <button
                            class="flex w-full cursor-pointer items-center justify-between gap-5 bg-transparent py-6 text-left text-[15px] font-bold text-[#2A2E38]"
                            onclick={() => openFaq = openFaq === i ? null : i}
                            aria-expanded={openFaq === i}
                        >
                            <span>{faq.question}</span>
                            <ChevronDown size={20} class={`shrink-0 transition-transform ${openFaq === i ? 'rotate-180' : ''}`}/>
                        </button>

                        {#if openFaq === i}
                            <div class="pb-6">
                                <p class="m-0 text-[13px] leading-8 text-[#777982]">{faq.answer}</p>
                            </div>
                        {/if}
                    </article>
                {/each}
            </div>
        </div>
    </section>

    <!-- CTA -->
    <section class="bg-[#2A2E38] px-6 py-20 text-center text-[#F5F1EE] md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#A8B79E]">08 — LOS GEHT'S</div>

        <h2 class="mx-auto my-8 max-w-[800px] text-4xl font-bold leading-tight tracking-[-2px] md:text-6xl">
            Die nächste Möglichkeit
            <span class="block text-[#62AA97]">wartet bereits.</span>
        </h2>

        <p class="mx-auto max-w-[600px] text-sm leading-8 text-[#C0C2C8]">
            Entdecke Dienstleistungen, veröffentliche deine Aufgaben
            oder finde neue Möglichkeiten auf NEXTJOB.
        </p>

        <div class="mt-8 flex flex-wrap justify-center gap-3.5">
            <a href="/register" class="inline-flex items-center justify-center gap-3 bg-[#62AA97] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#A8B79E] hover:text-[#2A2E38]">
                Konto erstellen <ArrowUpRight size={18}/>
            </a>

            <a href="/jobs" class="inline-flex items-center justify-center gap-3 border border-white/30 px-5 py-4 text-[13px] font-semibold text-[#F5F1EE] transition hover:bg-white hover:text-[#2A2E38]">
                Jobs ansehen <ArrowRight size={18}/>
            </a>
        </div>
    </section>

    <!-- FOOTER -->
    <footer class="bg-[#1F222B] px-6 pb-6 pt-16 text-[#F5F1EE] md:px-[6%]">
        <div class="grid gap-10 border-b border-white/10 pb-12 md:grid-cols-2 xl:grid-cols-4">
            <div>
                <a href="/" class="text-[27px] font-black tracking-[-1.5px] text-[#F5F1EE] no-underline">
                    NEXT<span class="text-[#62AA97]">JOB</span>
                </a>

                <p class="mt-5 max-w-[300px] text-[13px] leading-8 text-[#888B94]">
                    Eine digitale Plattform für lokale Dienstleistungen, Jobs und neue Möglichkeiten.
                </p>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">Plattform</h4>
                <a href="/jobs" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Jobs entdecken</a>
                <a href="/register" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Job veröffentlichen</a>
                <a href="/leaderboard" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Leaderboard</a>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">Informationen</h4>
                <a href="#how-it-works" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">So funktioniert's</a>
                <a href="#categories" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Dienstleistungen</a>
                <a href="#faq" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">FAQ</a>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">Account</h4>
                <a href="/login" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Login</a>
                <a href="/register" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">Registrieren</a>
            </div>
        </div>

        <div class="flex flex-col gap-4 pt-6 text-[11px] text-[#777982] md:flex-row md:justify-between">
            <p>© {new Date().getFullYear()} NEXTJOB</p>
            <p>Lokale Dienstleistungen. Digital verbunden.</p>
        </div>
    </footer>

</div>
