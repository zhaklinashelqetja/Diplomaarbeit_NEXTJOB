<script>
    let { data = [] } = $props();

    const chartWidth = 700;
    const chartHeight = 260;
    const left = 48;
    const right = 20;
    const top = 20;
    const bottom = 48;

    const monthNames = [
        'Jan.',
        'Feb.',
        'März',
        'Apr.',
        'Mai',
        'Juni',
        'Juli',
        'Aug.',
        'Sep.',
        'Okt.',
        'Nov.',
        'Dez.'
    ];

    let months = $derived(data ?? []);

    let maxValue = $derived(
        Math.max(1, ...months.map((item) => Number(item.new_users || 0)))
    );

    function formatMonth(monthString) {
        if (!monthString) return '';

        const [year, month] = monthString.split('-');
        const monthIndex = Number(month) - 1;

        if (monthIndex < 0 || monthIndex > 11) {
            return monthString;
        }

        return `${monthNames[monthIndex]} ${year}`;
    }

    function formatShortMonth(monthString) {
        if (!monthString) return '';

        const [, month] = monthString.split('-');
        const monthIndex = Number(month) - 1;

        if (monthIndex < 0 || monthIndex > 11) {
            return monthString;
        }

        return monthNames[monthIndex];
    }

    function getX(index) {
        if (months.length <= 1) {
            return left + (chartWidth - left - right) / 2;
        }

        return left + index * (chartWidth - left - right) / (months.length - 1);
    }

    function getY(value) {
        const chartArea = chartHeight - top - bottom;
        return top + chartArea - (Number(value || 0) / maxValue) * chartArea;
    }

    function getPath() {
        return months
            .map((item, index) => {
                const x = getX(index);
                const y = getY(item.new_users);
                return `${index === 0 ? 'M' : 'L'} ${x} ${y}`;
            })
            .join(' ');
    }

    let userPath = $derived(getPath());
</script>

<section class="rounded-2xl border border-[#2A2E38]/10 bg-white p-6 shadow-sm">
    <div class="mb-5">
        <h2 class="text-lg font-bold text-[#2A2E38]">
            Neue Nutzer pro Monat
        </h2>
        <p class="mt-1 text-sm text-[#2A2E38]/60">
            Entwicklung der monatlichen Registrierungen
        </p>
    </div>

    {#if months.length > 0}
        <div class="w-full overflow-x-auto">
            <svg
                viewBox={`0 0 ${chartWidth} ${chartHeight}`}
                class="w-full min-w-[500px]"
                role="img"
                aria-label="Diagramm mit neuen Nutzern pro Monat"
            >
                {#each [0, 1, 2, 3, 4] as step}
                    {@const y = top + step * (chartHeight - top - bottom) / 4}

                    <line
                        x1={left}
                        y1={y}
                        x2={chartWidth - right}
                        y2={y}
                        stroke="#2A2E38"
                        stroke-opacity="0.12"
                        stroke-dasharray="4 4"
                    />

                    <text
                        x={left - 10}
                        y={y + 4}
                        text-anchor="end"
                        font-size="11"
                        fill="#2A2E38"
                        opacity="0.6"
                    >
                        {Math.round(maxValue * (4 - step) / 4)}
                    </text>
                {/each}

                <path
                    d={userPath}
                    fill="none"
                    stroke="#8FB0C4"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />

                {#each months as month, index}
                    <circle
                        cx={getX(index)}
                        cy={getY(month.new_users)}
                        r="5"
                        fill="#8FB0C4"
                        stroke="white"
                        stroke-width="2"
                    >
                        <title>
                            {formatMonth(month.month)}: {month.new_users} neue Nutzer
                        </title>
                    </circle>

                    <text
                        x={getX(index)}
                        y={chartHeight - 28}
                        text-anchor="middle"
                        font-size="11"
                        fill="#2A2E38"
                    >
                        {formatShortMonth(month.month)}
                    </text>

                    {#if index === 0 || months[index - 1].month.split('-')[0] !== month.month.split('-')[0]}
                        <text
                            x={getX(index)}
                            y={chartHeight - 10}
                            text-anchor="middle"
                            font-size="10"
                            fill="#2A2E38"
                            opacity="0.65"
                        >
                            {month.month.split('-')[0]}
                        </text>
                    {/if}
                {/each}
            </svg>
        </div>
    {:else}
        <div class="rounded-xl bg-[#F5F1EE] px-4 py-8 text-center">
            <p class="text-sm text-[#2A2E38]/60">
                Noch keine Registrierungsdaten vorhanden.
            </p>
        </div>
    {/if}
</section>