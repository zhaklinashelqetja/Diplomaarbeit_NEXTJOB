
<script>
    import * as m from '$lib/paraglide/messages.js';
    import {
        ArrowUpRight, ArrowRight, Search, BriefcaseBusiness, Users,
        MessageCircle, Star, ShieldCheck, MapPin, ChevronDown,
        Wrench, Zap, Paintbrush, Construction, Trees, Sparkles,
        Monitor, Hammer, House
    } from '@lucide/svelte';

    let { data } = $props();
    let categoryTranslations = $derived({
        sanitaer: {
            name: m.landing_sanitaer_name(),
            description: m.landing_sanitaer_description(),
            examples: [
                m.landing_sanitaer_example1(),
                m.landing_sanitaer_example2(),
                m.landing_sanitaer_example3()
            ]
        },
        elektrotechnik: {
            name: m.landing_elektrotechnik_name(),
            description: m.landing_elektrotechnik_description(),
            examples: [
                m.landing_elektrotechnik_example1(),
                m.landing_elektrotechnik_example2(),
                m.landing_elektrotechnik_example3()
            ]
        },
        malerarbeiten: {
            name: m.landing_malerarbeiten_name(),
            description: m.landing_malerarbeiten_description(),
            examples: [
                m.landing_malerarbeiten_example1(),
                m.landing_malerarbeiten_example2(),
                m.landing_malerarbeiten_example3()
            ]
        },
        bau: {
            name: m.landing_bau_name(),
            description: m.landing_bau_description(),
            examples: [
                m.landing_bau_example1(),
                m.landing_bau_example2(),
                m.landing_bau_example3()
            ]
        },
        holzarbeiten: {
            name: m.landing_holzarbeiten_name(),
            description: m.landing_holzarbeiten_description(),
            examples: [
                m.landing_holzarbeiten_example1(),
                m.landing_holzarbeiten_example2(),
                m.landing_holzarbeiten_example3()
            ]
        },
        garten: {
            name: m.landing_garten_name(),
            description: m.landing_garten_description(),
            examples: [
                m.landing_garten_example1(),
                m.landing_garten_example2(),
                m.landing_garten_example3()
            ]
        },
        reinigung: {
            name: m.landing_reinigung_name(),
            description: m.landing_reinigung_description(),
            examples: [
                m.landing_reinigung_example1(),
                m.landing_reinigung_example2(),
                m.landing_reinigung_example3()
            ]
        },
        design: {
            name: m.landing_design_name(),
            description: m.landing_design_description(),
            examples: [
                m.landing_design_example1(),
                m.landing_design_example2(),
                m.landing_design_example3()
            ]
        },
        digital: {
            name: m.landing_digital_name(),
            description: m.landing_digital_description(),
            examples: [
                m.landing_digital_example1(),
                m.landing_digital_example2(),
                m.landing_digital_example3()
            ]
        }
    });

    let categories = $derived(
        data.categories.map(category => ({
            ...category,
            ...categoryTranslations[category.slug]
        }))
    );

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

    let faqs = $derived([
        {
            question: m.landing_faq1_question(),
            answer: m.landing_faq1_answer()
        },
        {
            question: m.landing_faq2_question(),
            answer: m.landing_faq2_answer()
        },
        {
            question: m.landing_faq3_question(),
            answer: m.landing_faq3_answer()
        },
        {
            question: m.landing_faq4_question(),
            answer: m.landing_faq4_answer()
        },
        {
            question: m.landing_faq5_question(),
            answer: m.landing_faq5_answer()
        },
        {
            question: m.landing_faq6_question(),
            answer: m.landing_faq6_answer()
        },
        {
            question: m.landing_faq7_question(),
            answer: m.landing_faq7_answer()
        }
    ]);
</script>

<svelte:head>
    <title>{m.landing_seo_title()}</title>
    <meta name="description" content={m.landing_seo_description()} />
    <meta name="keywords" content={m.landing_seo_keywords()} />
    <meta name="robots" content="index, follow" />
    <meta property="og:title" content={m.landing_seo_title()} />
    <meta property="og:description" content={m.landing_seo_description()} />
    <meta property="og:type" content="website" />
</svelte:head>

<div class="overflow-hidden bg-[#F5F1EE] text-[#2A2E38]">

    <!-- HERO -->
    <section class="grid items-center gap-14 px-6 py-20 md:px-[6%] lg:grid-cols-2 lg:gap-[5%] lg:py-24">
        <div>
            <div class="flex items-center gap-2.5 text-[11px] font-bold tracking-[2px] text-[#66766A]">
                <span class="h-2 w-2 bg-[#62AA97]"></span>
                {m.landing_badge()}
            </div>

            <h1 class="my-7 text-5xl font-extrabold leading-[0.99] tracking-[-3px] md:text-7xl lg:text-[85px] lg:tracking-[-5px]">
                {m.home_hero_title1()}
                <span class="block text-[#62AA97]">{m.landing_hero_right()}</span>
                {m.landing_hero_people()}
            </h1>

            <p class="max-w-[550px] text-base leading-8 text-[#656871]">
                {m.landing_hero_description()}
            </p>

            <div class="mt-8 flex flex-wrap gap-3.5">
                <a href="/jobs" class="inline-flex items-center justify-center gap-3 bg-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#62AA97]">
                    {m.search_discover_jobs()} <ArrowUpRight size={18}/>
                </a>

                <a href="/register" class="inline-flex items-center justify-center gap-3 border border-[#2A2E38] px-5 py-4 text-[13px] font-semibold text-[#2A2E38] transition hover:bg-[#2A2E38] hover:text-white">
                    {m.landing_publish_job()} <ArrowRight size={18}/>
                </a>
            </div>

            <div class="mt-8 flex items-center gap-2.5 text-xs text-[#85868B]">
                <MapPin size={16}/>
                {m.landing_local_tagline()}
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
                    <strong class="text-[13px]">{m.landing_opportunities()}</strong>
                    <p class="mt-1 text-[11px] text-[#85868B]">{m.landing_discover_offers()}</p>
                </div>
            </div>

            <div class="absolute bottom-8 right-[-10px] flex max-w-[290px] items-center gap-3.5 bg-white p-4 shadow-xl md:right-[-25px]">
                <div class="flex h-11 w-11 shrink-0 items-center justify-center bg-[#E1EAF0] text-[#587A91]">
                    <Users size={20}/>
                </div>
                <div>
                    <strong class="text-[13px]">{m.landing_connect_people()}</strong>
                    <p class="mt-1 text-[11px] text-[#85868B]">{m.landing_roles()}</p>
                </div>
            </div>

            <div class="absolute -bottom-9 left-0 text-[10px] tracking-[2px] text-[#777982]">
                <span class="text-[#62AA97]">01 /</span> {m.landing_local_services()}
            </div>
        </div>
    </section>

    <!-- INTRO -->
    <section class="bg-[#E9E6E1] px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_about_label()}</div>

        <div class="mt-10 grid gap-10 lg:grid-cols-2 lg:gap-[10%]">
            <h2 class="text-4xl leading-tight tracking-[-2px] md:text-5xl">
                {m.landing_intro_title1()}
                <span class="block text-[#62AA97]">{m.landing_intro_title2()}</span>
                {m.landing_intro_title3()}
            </h2>

            <div>
                <p class="mb-5 text-[15px] leading-8 text-[#656871]">
                    {m.landing_intro_text1()}
                </p>

                <p class="mb-5 text-[15px] leading-8 text-[#656871]">
                    {m.landing_intro_text2()}
                </p>

                <a href="#how-it-works" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                    {m.landing_learn_platform()} <ArrowRight size={18}/>
                </a>
            </div>
        </div>
    </section>

    <!-- HOW IT WORKS -->
    <section id="how-it-works" class="px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_how_label()}</div>

        <div class="mb-12 mt-9">
            <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">{m.landing_how_title()}</h2>
            <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                {m.landing_how_description()}
            </p>
        </div>

        <div class="grid grid-cols-1 border-y border-[#2A2E38]/20 md:grid-cols-2 lg:grid-cols-4">
            {#each [
                {number:'01',icon:Users,title:m.landing_step1_title(),text:m.landing_step1_text()},
                {number:'02',icon:Search,title:m.search_discover_jobs(),text:m.landing_step2_text()},
                {number:'03',icon:BriefcaseBusiness,title:m.landing_step3_title(),text:m.landing_step3_text()},
                {number:'04',icon:MessageCircle,title:m.landing_step4_title(),text:m.landing_step4_text()}
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
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_categories_label()}</div>

        <div class="mb-12 mt-9 flex flex-col items-start justify-between gap-6 lg:flex-row lg:items-end">
            <div>
                <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">{m.landing_categories_title()}</h2>
                <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                    {m.landing_categories_text()}
                </p>
            </div>

            <a href="/jobs" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                {m.landing_browse_jobs()} <ArrowRight size={18}/>
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
                            {m.search_discover_jobs()} <ArrowUpRight size={17}/>
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
                <span class="text-[11px] tracking-[2px] text-[#A8B79E]">{m.landing_for_employers()}</span>
                <p class="mb-0 text-xl">{m.landing_employer_image()}</p>
            </div>
        </div>

        <div>
            <div class="text-[11px] font-bold tracking-[2px] text-[#A8B79E]">{m.landing_employer_label()}</div>

            <h2 class="my-8 text-4xl font-bold leading-tight tracking-[-2px] md:text-5xl">
                {m.landing_employer_title1()}
                <span class="block text-[#62AA97]">{m.landing_employer_title2()}</span>
            </h2>

            <p class="mb-9 text-sm leading-8 text-[#C0C2C8]">
                {m.landing_employer_text()}
            </p>

            <div class="mb-9">
                {#each [
                    {title:m.landing_employer_step1(),text:m.landing_employer_step1_text()},
                    {title:m.landing_employer_step2(),text:m.landing_employer_step2_text()},
                    {title:m.landing_publish_job(),text:m.landing_employer_step3_text()},
                    {title:m.landing_employer_step4(),text:m.landing_employer_step4_text()},
                    {title:m.landing_employer_step5(),text:m.landing_employer_step5_text()}
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
                {m.landing_publish_now()} <ArrowUpRight size={18}/>
            </a>
        </div>
    </section>

    <!-- JOBNEHMER -->
    <section id="jobnehmer" class="grid gap-12 px-6 py-20 md:px-[6%] lg:grid-cols-2 lg:gap-[8%] lg:py-24">
        <div>
            <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_worker_label()}</div>

            <h2 class="my-8 text-4xl font-bold leading-tight tracking-[-2px] md:text-5xl">
                {m.home_pros_title1()}
                <span class="block text-[#62AA97]">{m.landing_worker_title2()}</span>
            </h2>

            <p class="mb-9 text-sm leading-8 text-[#777982]">
                {m.landing_worker_text()}
            </p>

            <div class="mb-9">
                {#each [
                    {title:m.landing_worker_step1(),text:m.landing_worker_step1_text()},
                    {title:m.landing_worker_step2(),text:m.landing_worker_step2_text()},
                    {title:m.landing_worker_step3(),text:m.landing_worker_step3_text()},
                    {title:m.landing_worker_step4(),text:m.landing_worker_step4_text()},
                    {title:m.landing_worker_step5(),text:m.landing_worker_step5_text()}
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
                {m.search_discover_jobs()} <ArrowUpRight size={18}/>
            </a>
        </div>

        <div class="relative min-h-[400px] bg-cover bg-center lg:min-h-[680px]"
            style="background-image: url('https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=85')">
            <div class="absolute bottom-6 left-6 right-6 bg-[#2A2E38]/85 p-6 text-white">
                <span class="text-[11px] tracking-[2px] text-[#A8B79E]">{m.landing_for_workers()}</span>
                <p class="mb-0 text-xl">{m.landing_worker_image()}</p>
            </div>
        </div>
    </section>

    <!-- FEATURES -->
    <section class="bg-[#E9E6E1] px-6 py-20 md:px-[6%]">
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_features_label()}</div>

        <div class="mb-12 mt-9">
            <h2 class="text-4xl font-bold tracking-[-2px] md:text-5xl">{m.landing_features_title()}</h2>
            <p class="mt-4 max-w-[550px] text-sm leading-7 text-[#777982]">
                {m.landing_features_text()}
            </p>
        </div>

        <div class="grid grid-cols-1 border-l border-t border-[#2A2E38]/20 md:grid-cols-2 xl:grid-cols-3">
            {#each [
                {icon:Search,title:m.landing_feature1(),text:m.landing_feature1_text()},
                {icon:Users,title:m.landing_feature2(),text:m.landing_feature2_text()},
                {icon:MessageCircle,title:m.landing_feature3(),text:m.landing_feature3_text()},
                {icon:Star,title:m.landing_feature4(),text:m.landing_feature4_text()},
                {icon:ShieldCheck,title:m.landing_feature5(),text:m.landing_feature5_text()},
                {icon:House,title:m.landing_feature6(),text:m.landing_feature6_text()}
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
        <div class="text-[11px] font-bold tracking-[2px] text-[#66766A]">{m.landing_faq_label()}</div>

        <div class="mt-9 grid gap-10 lg:grid-cols-[0.7fr_1.3fr] lg:gap-[10%]">
            <div>
                <h2 class="text-4xl font-bold leading-tight tracking-[-2px]">{m.landing_faq_title()}</h2>
                <p class="my-6 text-sm leading-8 text-[#777982]">
                    {m.landing_faq_text()}
                </p>

                <a href="/register" class="inline-flex items-center gap-2 border-b border-[#62AA97] pb-2 text-[13px] font-bold transition hover:text-[#62AA97]">
                    {m.landing_try_platform()} <ArrowRight size={18}/>
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
        <div class="text-[11px] font-bold tracking-[2px] text-[#A8B79E]">{m.landing_cta_label()}</div>

        <h2 class="mx-auto my-8 max-w-[800px] text-4xl font-bold leading-tight tracking-[-2px] md:text-6xl">
            {m.landing_cta_title1()}
            <span class="block text-[#62AA97]">{m.landing_cta_title2()}</span>
        </h2>

        <p class="mx-auto max-w-[600px] text-sm leading-8 text-[#C0C2C8]">
            {m.landing_cta_text()}
        </p>

        <div class="mt-8 flex flex-wrap justify-center gap-3.5">
            <a href="/register" class="inline-flex items-center justify-center gap-3 bg-[#62AA97] px-5 py-4 text-[13px] font-semibold text-white transition hover:bg-[#A8B79E] hover:text-[#2A2E38]">
                {m.register_title()} <ArrowUpRight size={18}/>
            </a>

            <a href="/jobs" class="inline-flex items-center justify-center gap-3 border border-white/30 px-5 py-4 text-[13px] font-semibold text-[#F5F1EE] transition hover:bg-white hover:text-[#2A2E38]">
                {m.landing_view_jobs()} <ArrowRight size={18}/>
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
                    {m.landing_footer_text()}
                </p>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">{m.landing_footer_platform()}</h4>
                <a href="/jobs" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.search_discover_jobs()}</a>
                <a href="/register" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.landing_publish_job()}</a>
                <a href="/leaderboard" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.landing_footer_leaderboard()}</a>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">{m.landing_footer_information()}</h4>
                <a href="#how-it-works" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.landing_footer_how()}</a>
                <a href="#categories" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.landing_footer_services()}</a>
                <a href="#faq" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">FAQ</a>
            </div>

            <div class="flex flex-col gap-4">
                <h4 class="mb-2 text-xs font-bold tracking-[1px] text-[#A8B79E]">{m.landing_footer_account()}</h4>
                <a href="/login" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.nav_login()}</a>
                <a href="/register" class="text-xs text-[#C0C2C8] transition hover:text-[#62AA97]">{m.nav_register()}</a>
            </div>
        </div>

        <div class="flex flex-col gap-4 pt-6 text-[11px] text-[#777982] md:flex-row md:justify-between">
            <p>© {new Date().getFullYear()} NEXTJOB</p>
            <p>{m.landing_footer_tagline()}</p>
        </div>
    </footer>

</div>
