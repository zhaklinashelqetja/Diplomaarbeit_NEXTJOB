
const categories = [
    {
        name: 'Sanitär & Installation',
        description:
            'Finde Fachkräfte für Wasserleitungen, Badezimmerinstallationen, Reparaturen, Armaturen und Sanitärarbeiten.',
        examples: ['Rohrreparaturen', 'Badinstallation', 'Armaturen'],
        slug: 'sanitaer'
    },
    {
        name: 'Elektrotechnik',
        description:
            'Finde Unterstützung bei elektrischen Installationen, Beleuchtung, Steckdosen, Wartung und Reparaturen.',
        examples: ['Beleuchtung', 'Elektroinstallation', 'Reparaturen'],
        slug: 'elektrotechnik'
    },
    {
        name: 'Malerarbeiten',
        description:
            'Suche Fachkräfte für Wandgestaltung, Innenanstriche, Fassaden, Renovierungen und Malerarbeiten.',
        examples: ['Wände streichen', 'Fassaden', 'Renovierungen'],
        slug: 'malerarbeiten'
    },
    {
        name: 'Bau & Renovierung',
        description:
            'Finde Unterstützung für Bauarbeiten, Fliesen, Maurerarbeiten, Reparaturen und Renovierungsprojekte.',
        examples: ['Fliesenlegen', 'Maurerarbeiten', 'Renovierung'],
        slug: 'bau'
    },
    {
        name: 'Holzarbeiten',
        description:
            'Entdecke Dienstleistungen rund um Möbel, Türen, Holzreparaturen, maßgeschneiderte Möbel und Tischlerarbeiten.',
        examples: ['Möbel', 'Türen', 'Holzreparaturen'],
        slug: 'holzarbeiten'
    },
    {
        name: 'Garten & Außenbereich',
        description:
            'Finde Hilfe für Gartenpflege, Rasenmähen, Pflanzen, Außenanlagen und weitere Gartenarbeiten.',
        examples: ['Gartenpflege', 'Rasenmähen', 'Pflanzen'],
        slug: 'garten'
    },
    {
        name: 'Reinigung',
        description:
            'Suche Reinigungskräfte für Wohnungen, Büros, Fenster, regelmäßige Reinigung und weitere Aufgaben.',
        examples: ['Wohnungsreinigung', 'Büroreinigung', 'Fenster'],
        slug: 'reinigung'
    },
    {
        name: 'Grafik & Design',
        description:
            'Finde kreative Unterstützung für Poster, Logos, Grafiken, Social-Media-Inhalte und visuelle Projekte.',
        examples: ['Poster', 'Logos', 'Social Media'],
        slug: 'design'
    },
    {
        name: 'Web & Digital',
        description:
            'Entdecke digitale Dienstleistungen wie Webseiten, digitale Unterstützung, Online-Projekte und technische Aufgaben.',
        examples: ['Webseiten', 'Technische Hilfe', 'Digitale Projekte'],
        slug: 'digital'
    }
];

export function load() {
    return {
        seo: {
            title: 'NEXTJOB – Lokale Dienstleistungen und Jobs finden',
            description:
                'Entdecke lokale Dienstleistungen, finde passende Jobs oder veröffentliche deine eigenen Aufträge auf NEXTJOB. Verbinde Jobgeber und Jobnehmer einfach digital.',
            keywords:
                'NEXTJOB, lokale Dienstleistungen, Jobs Shkodra, Handwerker finden, Jobs finden, Dienstleistungen anbieten'
        },
        categories
    };
}
